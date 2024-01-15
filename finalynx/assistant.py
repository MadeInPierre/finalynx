import json
import os
from datetime import date
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import finalynx.theme
from docopt import docopt  # type: ignore[import]
from finalynx import Dashboard
from finalynx import Fetch
from finalynx import Portfolio
from finalynx.budget.budget import Budget
from finalynx.config import get_active_theme as TH
from finalynx.config import set_active_theme
from finalynx.copilot.recommendations import render_recommendations
from finalynx.fetch.source_base_line import SourceBaseLine
from finalynx.fetch.source_finary import SourceFinary
from finalynx.portfolio.bucket import Bucket
from finalynx.portfolio.envelope import Envelope
from finalynx.portfolio.folder import Sidecar
from finalynx.simulator.timeline import Simulation
from finalynx.simulator.timeline import Timeline
from html2image import Html2Image  # type: ignore[import]
from rich import inspect  # noqa F401
from rich import pretty
from rich import print  # noqa F401
from rich import traceback
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.text import Text
from rich.tree import Tree

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
        # Main structure elements
        portfolio: Portfolio,
        buckets: Optional[List[Bucket]] = None,
        envelopes: Optional[List[Envelope]] = None,
        # Portfolio options
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
        # Budget options
        check_budget: bool = False,
        interactive: bool = False,
        # Simulation options
        simulation: Optional[Simulation] = None,
    ):
        self.portfolio = portfolio
        self.buckets = buckets if buckets else []
        self.envelopes = envelopes if envelopes else []

        # Options that can either be set in the constructor or from the command line options, see --help
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
        self.check_budget = check_budget
        self.interactive = interactive
        self.simulation = simulation

        # Set the global color theme if specified
        if theme:
            set_active_theme(theme)

        # Unless disabled, parse the command line options as an additional source of settings
        if not ignore_argv:
            self._parse_args()

        # Create the fetching manager instance
        self._fetch = Fetch(self.portfolio, self.clear_cache, self.ignore_orphans)
        self.budget = Budget()

        # Initialize the simulation timeline with the initial user events
        self._timeline = Timeline(simulation, self.portfolio, self.buckets) if simulation else None

        # Store the portfolio renders for each simulation date (if enabled)
        self._timeline_renders: List[Any] = []

    def add_source(self, source: SourceBaseLine) -> None:
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
        if args["budget"]:
            self.check_budget = True
        if args["--interactive"]:
            if not self.check_budget:
                console.log("[red][bold]Error:[/] --interactive can only be used with budget, ignoring.")
            self.interactive = True
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
        if args["--future"] and self.simulation:
            self.simulation.print_final = True
        if args["--each-step"] and self.simulation:
            self.simulation.print_each_step = True
        if args["--sim-steps"] and self.simulation:
            self.simulation.step_years = int(args["--sim-steps"])
        if args["--metric-frequency"] and self.simulation:
            self.simulation.metrics_record_frequency = str(args["--metric-frequency"])
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

        # Fetch the budget from N26 if enabled
        if self.check_budget:
            fetched_tree.add(self.budget.fetch(self.clear_cache, self.force_signin))
            console.log("[bold]Tip:[/] run again with -I or --interactive review the expenses 👀")

        # Render the console elements
        main_frame = self.render_mainframe()
        dict_panels, render_panels = self.render_panels()
        renders: List[Any] = [main_frame, render_panels]
        if self.check_budget:
            renders.append(self.budget.render_expenses())

        # Save the current portfolio to a file. Useful for statistics later
        if self.enable_export:
            self.export_json(self.export_dir)

        # Show the data fetched from Finary if specified
        if self.show_data:
            console.print(Panel(fetched_tree, title="Fetched data"))

        # Run the simulation if there are events defined
        if self.simulation:
            # Add the simulation summary to the performance panel in the console
            dict_panels["performance"].add(self.simulate())

            # If enabled by the user, print the portfolio at each simulation date
            if self.simulation.print_each_step:
                for element in self._timeline_renders:
                    renders.append(element)

            # If enabled by the user, print the final portfolio after the simulation
            if self.simulation.print_final:
                renders.append(f"\nYour portfolio in {self.simulation.end_date}:")
                renders.append(self.render_mainframe())
            else:
                end_year = self.simulation.end_date.year if self.simulation.end_date else date.today().year + 100
                console.log(f"    [bold]Tip:[/] Use --future to display the final portfolio in {end_year}.\n")

        # Display the entire portfolio and associated recommendations
        for render in renders:
            console.print("\n\n", render)
        console.print("\n")

        # Interactive review of the budget expenses if enabled
        if self.check_budget and self.interactive:
            self.budget.interactive_review()

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

    def simulate(self) -> Tree:
        """Simulate your portfolio's future with the `Simulation` configuration
        passed in the `Assistant` constructor.
        :returns: A tree with the portfolio total worth every few years until the end date.
        """
        if not (self.simulation and self._timeline and not self._timeline.is_finished):
            raise ValueError("Nothing to simulate, have you added events?")

        console.log("Launching simulation...")
        tree = Tree("\n[bold]Worth", guide_style=TH().TREE_BRANCH)

        # Utility function to append a new formatted line to the tree
        def append_worth(year: int, amount: float) -> None:
            tree.add(f"[{TH().TEXT}]{year}:       [{TH().ACCENT}][bold]{round(amount / 1000):>4}[/] k€")

        # Run the simulation and append the results to the tree every `step_years`
        append_worth(date.today().year, self.portfolio.get_amount())
        for year in track(
            range(date.today().year + 1, self._timeline.end_date.year),
            description=f"Simulating until [{TH().ACCENT} bold]{self._timeline.end_date}[/]...",
        ):
            self._timeline.goto(date(year, 12, 31))

            if (year - date.today().year) % self.simulation.step_years == 0:
                # Append the portfolio's worth to the Worth tree
                append_worth(year, self.portfolio.get_amount())

                # Render each intermediate simulation step
                if self.simulation.print_each_step:
                    title = "Your portfolio in [bold]" + str(year) + "-12-31:[/]"
                    self._timeline_renders.append(Panel(self.render_mainframe(), title=title))

        # Run until the end date and append the final result
        self._timeline.run()
        append_worth(self._timeline.current_date.year, self.portfolio.get_amount())
        console.log(f"    Portfolio will be worth [{TH().ACCENT}]{self.portfolio.get_amount():.0f} €[/]")
        return tree

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

    def render_panels(self) -> Tuple[Dict[str, Any], Columns]:
        """Renders the default set of panels used in the default console view when calling run()."""

        def panel(title: str, content: Any) -> Panel:
            return Panel(content, title=title, padding=(1, 2), expand=False, border_style=TH().PANEL)

        dict_items: Dict[str, Any] = {
            "recommendations": render_recommendations(self.portfolio, self.envelopes),
            "performance": self.render_performance_report(),
        }

        # Add the budget panel if enabled
        if self.check_budget:
            dict_items["budget"] = self.budget.render_summary()

        return dict_items, Columns(
            [Text(" ")] + [panel(k.capitalize(), v) for k, v in dict_items.items()], padding=(2, 2)
        )

    def render_performance_report(self) -> Tree:
        """Print the current and ideal global expected performance. Call either run() or initialize() first."""
        perf = self.portfolio.get_perf(ideal=False).expected
        perf_ideal = self.portfolio.get_perf(ideal=True).expected

        tree = Tree("Global Performance", hide_root=True, guide_style=TH().TREE_BRANCH)
        node = tree.add("[bold]Yield")
        node.add(f"[{TH().TEXT}]Current:    [bold][{TH().ACCENT}]{perf:.2f} %[/] / year")
        node.add(f"[{TH().TEXT}]Planned:    [bold][{TH().ACCENT}]{perf_ideal:.2f} %[/] / year")

        if self.simulation:
            node.add(f"[{TH().TEXT}]Inflation:  [bold][gold1]{self.simulation.inflation:.2f} %[/] / year")
        return tree

    def dashboard(self) -> None:
        """Launch an interactive web dashboard! Call either run() or initialize() first."""
        console.log("Launching dashboard.")
        Dashboard(hide_amounts=self.hide_amounts).run(self.portfolio, self._timeline)

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
            console.log("[yellow][bold]Warning:[/] Can't find the folder to save the portfolio to JSON. Three options:")
            console.log("[yellow]  1. Disable export using --no-export")
            console.log("[yellow]  2. Create a folder called logs/ in this folder (default folder)")
            console.log("[yellow]  3. Set your own export directory using --export-dir=your/path/to/dir/")

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
        dashboard_console.print(self.render_panels()[1])
        output_html = dashboard_console.export_html().replace("body {", f"body {{\n    zoom: {zoom};")

        # Convert the HTML to PNG
        try:
            Html2Image(output_path=full_path).screenshot(html_str=output_html, save_as=file_name, size=size)
            console.print(f"Saved portfolio PNG to '{full_path + file_name}'")
        except Exception as e:
            console.log(f"[red][bold]Error:[/] Package html2image failed, skipping ({e})")

        # Restore theme and return the image path
        set_active_theme(previous_theme)
        return full_path + file_name
