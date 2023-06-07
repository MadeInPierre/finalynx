import json
import os
from datetime import date
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import TYPE_CHECKING

import finalynx.theme
from docopt import docopt
from finalynx import Dashboard
from finalynx import Fetch
from finalynx import Portfolio
from finalynx.config import DEFAULT_CURRENCY
from finalynx.config import get_active_theme as TH
from finalynx.config import set_active_theme
from finalynx.fetch.source_base import SourceBase
from finalynx.fetch.source_finary import SourceFinary
from finalynx.portfolio.bucket import Bucket
from finalynx.portfolio.envelope import Envelope
from finalynx.portfolio.folder import Folder
from finalynx.portfolio.folder import FolderDisplay
from finalynx.portfolio.folder import SharedFolder
from finalynx.portfolio.folder import Sidecar
from finalynx.portfolio.node import Node
from finalynx.portfolio.targets import Target
from html2image import Html2Image
from rich import inspect  # noqa F401
from rich import pretty
from rich import print  # noqa F401
from rich import traceback
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree


if TYPE_CHECKING:
    from rich.console import ConsoleRenderable

from .__meta__ import __version__
from .console import console
from .usage import __doc__

# Enable rich's features

traceback.install()
pretty.install()


class Assistant:
    """Main entry class that orchestrates the generation of your selected outputs.

    Declare your portfolio configuration (and other extensions
    such as scenario and copilot) in a separate file and create an instance
    of this `Assistant` class with your configuration as input.

    :param portfolio: Your fully defined portfolio structure (with `Target`, `Folder` and `Line` objects).
    :param scenario: Your simulation configuration including `Event` objects and so on _(TODO coming soon)_.
    :param copilot: Your investment strategy configuration _(TODO coming soon)_.

    :param ignore_orphans: Ignore fetched lines that you didn't reference in your portfolio, defaults to False.
    :param force_signin: Sign in to Finary even if there is an existing cookies file, defaults to False.
    :param hide_amount: Display your portfolio with dots instead of the real values (easier to share), defaults to False.
    :param hide_root: Display your portfolio without the root (cosmetic preference), defaults to False.
    """

    def __init__(
        self,
        portfolio: Portfolio,
        buckets: Optional[List[Bucket]] = None,
        envelopes: Optional[List[Envelope]] = None,
        ignore_orphans: bool = False,
        clear_cache: bool = False,
        force_signin: bool = False,
        hide_amounts: bool = False,
        hide_root: bool = False,
        show_data: bool = False,
        launch_dashboard: bool = False,
        output_format: str = "[console]",
        enable_export: bool = True,
        export_dir: str = "logs",
        active_sources: Optional[List[str]] = None,
        theme: Optional[finalynx.theme.Theme] = None,
        sidecars: Optional[List[Sidecar]] = None,
        ignore_argv: bool = False,
    ):
        self.portfolio = portfolio
        self.buckets = buckets if buckets else []
        self.envelopes = envelopes if envelopes else []

        # Options that can either be set in the constructor or from the command line options, type --help
        self.ignore_orphans = ignore_orphans
        self.clear_cache = clear_cache
        self.force_signin = force_signin
        self.hide_amounts = hide_amounts
        self.hide_root = hide_root
        self.show_data = show_data
        self.launch_dashboard = launch_dashboard
        self.output_format = output_format
        self.enable_export = enable_export
        self.export_dir = export_dir
        self.active_sources = active_sources if active_sources else ["finary"]
        self.sidecars = sidecars if sidecars else []

        # Set the global color theme if specified
        if theme:
            set_active_theme(theme)

        # Unless disabled, parse the command line options as an additional source of settings
        if not ignore_argv:
            self._parse_args()

        # Create the fetching manager instance
        self._fetch = Fetch(self.portfolio, self.clear_cache, self.ignore_orphans)

    def add_source(self, source: SourceBase) -> None:
        """Register a source, either defined in your own config or from the available Finalynx sources
        using `from finalynx.fetch.source_any import SourceAny`."""
        self._fetch.add_source(source)

    def _parse_args(self) -> None:
        """Internal method that parses the command-line options and activates the options
        in the corresponding modules.
        """
        args = docopt(__doc__, version=__version__)  # type: ignore
        if args["--ignore-orphans"]:
            self.ignore_orphans = True
        if args["--clear-cache"]:
            self.clear_cache = True
        if args["--force-signin"]:
            self.clear_cache = True
            self.force_signin = True
        if args["--hide-amounts"]:
            self.hide_amounts = True
        if args["--hide-root"]:
            self.hide_root = True
        if args["--show-data"]:
            self.show_data = True
        if args["dashboard"]:
            self.launch_dashboard = True
        if args["--format"]:
            self.output_format = args["--format"]
        if args["--sidecar"]:
            for sidecar in list(args["--sidecar"]):
                if sidecar.count(",") > 3:
                    console.log(
                        "[red]Error: invalid sidecar format, skipping. Use at most 3 ',' to"
                        " define format, condition, title and/or folder rendering.",
                        highlight=False,
                    )
                    continue
                self.sidecars.append(Sidecar(*sidecar.split(",")))
        if args["delta"]:
            self.output_format = "[console_delta]"
            self.sidecars = [s for s in self.sidecars if s.output_format != "[delta]"]
        if args["perf"]:
            self.output_format = "[console_perf]"
            self.sidecars = [s for s in self.sidecars if s.output_format != "[perf]"]
        if args["ideal"]:
            self.output_format = "[console_ideal]"
            self.sidecars = [s for s in self.sidecars if s.output_format != "[ideal]"]
        if args["target"]:
            self.output_format = "[console_target]"
            self.sidecars = [s for s in self.sidecars if s.output_format != "[target]"]
        if args["text"]:
            self.output_format = "[text]"
        if args["--no-export"]:
            self.enable_export = False
        if args["--export-dir"]:
            self.export_dir = args["--export-dir"]
        if args["--sources"]:
            self.active_sources = str(args["--sources"]).split(",")
        if args["--theme"]:
            theme_name = str(args["--theme"])
            if theme_name not in finalynx.theme.AVAILABLE_THEMES:
                raise ValueError("Theme name options: " + ", ".join(finalynx.theme.AVAILABLE_THEMES.keys()))
            set_active_theme(finalynx.theme.AVAILABLE_THEMES[theme_name]())

    def run(self) -> None:
        """Main method to run (once your configuration is fully defined). This method orchestrates the call
        to the other available methods in this class. This methods displays a nice default output.

        This method will fetch the data from your Finary account, process the targets in the portfolio tree,
        run your simulation, generate recommendations, and format the output nicely to the console.
        """

        # Fetch from the online sources and process the portfolio
        fetched_tree = self.initialize()

        # Render the console elements
        main_frame = self.render_mainframe()
        panels = self.render_panels()

        # Save the current portfolio to a file. Useful for statistics later
        if self.enable_export:
            self.export_json(self.export_dir)

        # Show the data fetched from Finary if specified
        if self.show_data:
            console.print(Panel(fetched_tree, title="Fetched data"))

        # Display the entire portfolio and associated recommendations
        console.print(
            "\n\n",
            main_frame,
            "\n\n",
            panels,
            "\n",
        )

        # Host a local webserver with the running dashboard
        if self.launch_dashboard:
            self.dashboard()

    def initialize(self) -> Tree:
        """Fetch investments online from all sources and process the portfolio internally.
        Call this method first if you're not using run()."""

        # Add default sources based on user input
        if "finary" in self.active_sources:
            self._fetch.add_source(SourceFinary(self.force_signin))

        # Launch the fetching process and fill tree with current valuations fetched from Finary
        fetched_tree = self._fetch.fetch_from(self.active_sources)

        # Mandatory step after fetching to process some targets and buckets
        self.portfolio.process()

        # Validate processing results
        for _ in [b for b in self.buckets if b.get_used_amount() != b.get_max_amount()]:
            console.log("[yellow][bold]Warning:[/] Bucket's total amount was not fully used.")

        return fetched_tree

    def render_mainframe(self) -> Columns:
        """Renders the main tree and sidecars together. Call either run() or initialize() first."""

        # Items to be rendered as a row
        main_frame = [
            Text("   "),
            self.portfolio.tree(
                output_format=self.output_format,
                hide_root=self.hide_root,
                hide_amounts=self.hide_amounts,
            ),
        ]

        # Display deltas only if not already printed in the main tree
        main_frame += [Text("     ")] + [self.portfolio.render_sidecar(s, self.hide_root) for s in self.sidecars]

        return Columns(main_frame, padding=(0, 0))  # type: ignore

    def render_panels(self) -> Columns:
        """Renders the default set of panels used in the default console view when calling run()."""

        # Final set of results to be displayed
        panels: List[ConsoleRenderable] = [
            Text(" "),
            Panel(
                self.render_recommendations(),
                title="Recommendations",
                padding=(1, 2),
                expand=False,
                border_style=TH().PANEL,
            ),
            Panel(
                self.render_performance_report(),
                title="Performance",
                padding=(1, 2),
                expand=False,
                border_style=TH().PANEL,
            ),
        ]

        return Columns(panels, padding=(2, 2))

    def render_performance_report(self) -> Tree:
        """Print the current and ideal global expected performance. Call either run() or initialize() first."""
        perf = self.portfolio.get_perf(ideal=False).expected
        perf_ideal = self.portfolio.get_perf(ideal=True).expected

        tree = Tree("Global Performance", hide_root=True)
        tree.add(f"[{TH().TEXT}]Current:  [bold][{TH().ACCENT}]{perf:.1f} %[/] / year")
        tree.add(f"[{TH().TEXT}]Planned:  [bold][{TH().ACCENT}]{perf_ideal:.1f} %[/] / year")
        return tree

    def render_recommendations(self) -> Tree:
        """Sort lines with non-zero deltas by envelopes and display them as a summary of transfers to make.
        Call either run() or initialize() first.
        """
        dict_envs: Dict[str, Any] = {}

        # Guide the user to set envelopes if not already done
        if not self.envelopes:
            return Tree(
                f"[dim {TH().TEXT}]"
                "To activate recommendations, set\n"
                "envelopes to your lines and give\n"
                "them to Assistant (tutorial #11)"
            )

        # Find all folders with non-zero deltas and non-zero amounts (to avoid empty shared folders)
        def _get_folders(node: Folder) -> List[Folder]:
            found: List[Folder] = []
            for child in node.children:
                if isinstance(child, SharedFolder):
                    if child.get_amount() > 0:
                        found.append(child)
                elif isinstance(child, Folder):
                    if child.display == FolderDisplay.EXPANDED:
                        found += _get_folders(child)
                    else:
                        found.append(child)
            return found

        # Check if a folder has non-zero deltas to be displayed in the recommendations
        def _check_node(node: Node) -> bool:
            return node.get_delta() != 0 and node.target.check() not in [
                Target.RESULT_NONE,
                Target.RESULT_OK,
                Target.RESULT_TOLERATED,
            ]

        # Render each envelope of folder's parent with a custom style along with the
        def _render_title(children: List[Any], name: str) -> Tuple[int, str]:
            total_delta = round(sum([c.get_delta() for c in children]))
            return total_delta, (
                f"[{TH().DELTA_POS if total_delta > 0 else TH().DELTA_NEG}]"
                f"{'+' if total_delta > 0 else ''}{total_delta} {DEFAULT_CURRENCY} "
                f"[{TH().FOLDER_COLOR} {TH().FOLDER_STYLE}]{name}[/]"
            )

        # For each envelope, find all lines with non-zero deltas
        for envelope in self.envelopes:
            if lines := [line for line in envelope.lines if _check_node(line)]:
                delta, title = _render_title(lines, envelope.name)
                dict_envs[title] = (delta, lines)

        # Render folders with non-zero deltas, classify them by parent name
        if folders := [f for f in _get_folders(self.portfolio) if _check_node(f)]:
            for parent_name in {f.parent.name for f in folders if f.parent}:
                items = [f for f in folders if f.parent and f.parent.name == parent_name]
                delta, title = _render_title(items, parent_name)
                dict_envs[title] = (delta, items)

        # Render the tree with folders containing lines with non-zero deltas (sorted by delta)
        tree = Tree("Envelopes", hide_root=True, guide_style=TH().TREE_BRANCH)
        dict_sorted = {k: v[1] for k, v in sorted(dict_envs.items(), key=lambda item: item[1][0])}  # type: ignore
        for i_env, envelope_name in enumerate(dict_sorted):
            node = tree.add(envelope_name)
            for i_line, line in enumerate(dict_sorted[envelope_name]):
                render = f"[{TH().TEXT}]{line._render_delta(children=dict_sorted[envelope_name])}{line._render_name()}"  # type: ignore
                newline = bool(i_line == len(dict_sorted[envelope_name]) - 1 and i_env < len(dict_envs.keys()) - 1)
                node.add(render + ("\n" if newline else ""))

        # If no envelopes are displayed, show a nice message instead
        if not tree.children:
            tree.add("You're on track! 🎉")
        return tree

    def dashboard(self) -> None:
        """Launch an interactive web dashboard! Call either run() or initialize() first."""
        console.log("Launching dashboard.")
        Dashboard(hide_amounts=self.hide_amounts).run(portfolio=self.portfolio)

    def export_json(self, dirpath: str) -> None:
        """Save everything in a JSON file. Can be used for data analysis in future
        or by other projects.
        :param dirpath: Path to the directory where the file will be saved.
        """
        today = date.today().isoformat()
        full_path = os.path.join(dirpath, f"finalynx_{today}.json")

        final_dict = {
            "date": today,
            "envelopes": [e.to_dict() for e in self.envelopes],
            "buckets": [b.to_dict() for b in self.buckets],
            "portfolio": self.portfolio.to_dict(),
        }

        try:
            with open(full_path, "w") as f:
                f.write(json.dumps(final_dict, indent=4))
            console.log(f"Saved current portfolio to '{full_path}'")
        except FileNotFoundError:
            console.log("[red][bold]Error:[/] Can't find the folder to save the portfolio to JSON. Three options:")
            console.log("[red]  1. Disable export using --no-export")
            console.log("[red]  2. Create a folder called logs/ in this folder (default folder)")
            console.log("[red]  3. Set your own export directory using --export-dir=your/path/to/dir/")

    def export_img(
        self,
        dir_path: str = "",
        file_name: str = "portfolio.png",
        size: Tuple[int, int] = (1300, 2300),
        zoom: float = 2,
    ) -> str:
        """Export your portfolio to a PNG file with the following options:
        :param dir_path: Relative path to the directory that will contain the
        :param file_name: File name without the path, must end with .png
        :param size: Output image resolution.
        :param zoom: Image zoom, only way to affect the DPI of the image.
        :returns: The full absolute path where the image was saved.
        """
        # Create the directory if it does not exist
        full_path = os.path.join(os.getcwd(), dir_path)
        os.makedirs(full_path, exist_ok=True)

        # Temporarily change the current theme to the web theme
        previous_theme = TH()
        set_active_theme(finalynx.theme.DashboardTheme())

        # Export the entire portfolio tree to HTML and set the zoom
        dashboard_console = Console(record=True, file=open(os.devnull, "w"))
        dashboard_console.print(self.render_mainframe())
        dashboard_console.print(self.render_panels())
        output_html = dashboard_console.export_html().replace("body {", f"body {{\n    zoom: {zoom};")

        # Convert the HTML to PNG
        Html2Image(output_path=full_path).screenshot(html_str=output_html, save_as=file_name, size=size)

        # Restore theme and return the image path
        set_active_theme(previous_theme)
        console.print(f"Saved portfolio PNG to '{full_path + file_name}'")
        return full_path + file_name
