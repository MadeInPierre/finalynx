import json
import os
from datetime import date
from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from docopt import docopt
from finalynx import Dashboard
from finalynx import FetchFinary
from finalynx import Portfolio
from finalynx.config import DEFAULT_CURRENCY
from finalynx.portfolio.bucket import Bucket
from finalynx.portfolio.envelope import Envelope
from finalynx.portfolio.folder import Folder
from finalynx.portfolio.folder import FolderDisplay
from finalynx.portfolio.folder import SharedFolder
from finalynx.portfolio.targets import Target
from rich import inspect  # noqa F401
from rich import pretty
from rich import print  # noqa F401
from rich import traceback
from rich.columns import Columns
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
        hide_deltas: bool = False,
        launch_dashboard: bool = False,
        output_format: str = "[console]",
        enable_export: bool = True,
        export_dir: str = "logs",
    ):
        self.portfolio = portfolio
        self.buckets = buckets if buckets else []
        self.envelopes = envelopes if envelopes else []

        # Options that can either be set in the constructor or from the command line
        self.ignore_orphans = ignore_orphans
        self.clear_cache = clear_cache
        self.force_signin = force_signin
        self.hide_amounts = hide_amounts
        self.hide_root = hide_root
        self.show_data = show_data
        self.launch_dashboard = launch_dashboard
        self.output_format = output_format
        self.hide_deltas = hide_deltas
        self.enable_export = enable_export
        self.export_dir = export_dir

        self._parse_args()

    def _parse_args(self) -> None:
        """Internal method that parses the command-line options and activates the options
        in the corresponding modules.
        """
        args = docopt(__doc__, version=__version__)
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
        if args["deltas"]:
            self.output_format = "[console_deltas]"
        if args["perf"]:
            self.output_format = "[console_perf]"
        if args["ideal"]:
            self.output_format = "[console_ideal]"
        if args["targets"]:
            self.output_format = "[console_targets]"
            self.hide_deltas = True
        if args["text"]:
            self.output_format = "[text]"
            self.hide_deltas = True
        if args["--hide-deltas"]:
            self.hide_deltas = True
        if args["--no-export"]:
            self.enable_export = False
        if args["--export-dir"]:
            self.export_dir = args["--export-dir"]

    def run(self) -> None:
        """Main function to run once your configuration is fully defined.

        This function will fetch the data from your Finary account, process the thr targets in the portfolio tree,
        run your simulation, generate recommendations, and format the output nicely to the console.
        """

        # Fill tree with current valuations fetched from Finary
        finary_tree = FetchFinary(self.portfolio, self.clear_cache, self.force_signin, self.ignore_orphans).fetch()

        # Mandatory step after fetching to process some targets and buckets
        self.portfolio.process()

        # Simulate the portolio's evolution through the years by auto-investing each month
        # simulation = self.scenario.rich_simulation(self.portfolio)  # noqa TODO

        # Get recommendations for immediate investment operations
        # recommentations = self.copilot.rich_recommendations(self.portfolio)  # noqa TODO

        # Items to be rendered as a row
        render = [
            Text(" "),
            self.portfolio.tree(
                output_format=self.output_format,
                hide_root=self.hide_root,
                hide_amounts=self.hide_amounts,
            ),
        ]

        # Display deltas only if not already printed in the main tree
        if not self.hide_deltas and "delta" not in self.output_format:
            render.append(self.portfolio.tree_delta())

        # Final set of results to be displayed
        panels: List[ConsoleRenderable] = [
            Panel(self.render_envelopes(), title="Delta Investments", padding=(1, 2), expand=False),
            Panel(self.render_perf(), title="Performance", padding=(1, 2), expand=False),
        ]

        # Show the data fetched from Finary if specified
        if self.show_data:
            panels.append(Panel(finary_tree, title="Finary data"))

        # Save the current portfolio to a file. Useful for statistics later
        if self.enable_export:
            self.export(self.export_dir)

        # Display the entire portfolio and associated recommendations
        console.print("\n", Columns(render, padding=(2, 2)), "\n")  # type: ignore
        console.print(Columns(panels, padding=(2, 2)), "\n")

        # Host a local webserver with the running dashboard
        if self.launch_dashboard:
            console.log("Launching dashboard.")
            Dashboard(hide_amounts=self.hide_amounts).run(portfolio=self.portfolio)

    def render_perf(self) -> Tree:
        """Print the current and ideal global expected performance."""
        perf = self.portfolio.get_perf(ideal=False).expected
        perf_ideal = self.portfolio.get_perf(ideal=True).expected

        tree = Tree("Global Performance", hide_root=True)
        tree.add(f"Current:  [bold][green]{perf:.1f} %[/] / year")
        tree.add(f"Planned:  [bold][green]{perf_ideal:.1f} %[/] / year")

        console.log(
            f"""Your global portfolio's performance is {perf:.1f}%/yr, follow your targets to get {perf_ideal:.1f}%/yr."""
        )
        return tree

    def render_envelopes(self) -> Tree:
        """Sort lines with non-zero deltas by envelopes and display them as
        a summary of transfers to make."""
        tree = Tree("Envelopes", hide_root=True)

        for env in self.envelopes:
            children, env_delta = [], 0.0
            for line in env.lines:
                delta = line.get_delta()
                if delta != 0 and line.target.check() not in [
                    Target.RESULT_NONE,
                    Target.RESULT_OK,
                    Target.RESULT_TOLERATED,
                ]:
                    env_delta += delta
                    children.append(line._render_delta(children=env.lines) + line._render_name())

            if children:
                env_delta = round(env_delta)
                render_delta = f"[{'green' if env_delta > 0 else 'red'}]{'+' if env_delta > 0 else ''}{env_delta} {DEFAULT_CURRENCY}"
                node = tree.add(f"{render_delta} [dodger_blue2 bold]{env.name}[/]")
                for child in children:
                    node.add(child)
                node.children[-1].label += "\n"  # type: ignore

        def _get_folders(node: Folder) -> List[Folder]:
            found: List[Folder] = []
            for child in node.children:
                if isinstance(child, Folder):
                    if isinstance(child, SharedFolder):
                        found.append(child)
                    elif child.display == FolderDisplay.EXPANDED:
                        found += _get_folders(child)
                    else:
                        found.append(child)
            return found

        folders = _get_folders(self.portfolio)
        if folders:
            node = tree.add("[dodger_blue2 bold]Folders")
            for f in folders:
                if f.get_delta() != 0:
                    node.add(f._render_delta(children=folders) + f._render_name())
        return tree

    def export(self, dirpath: str) -> None:
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
            console.log(
                """[red][bold]Error:[/] Can't find the folder to save the portfolio to JSON. Three options:
1. Disable export using --no-export
2. Create a folder called logs/ in this folder (default folder)
3. Set your own export directory using --export-dir=your/path/to/dir/
            """
            )
