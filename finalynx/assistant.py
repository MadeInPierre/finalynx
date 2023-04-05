from typing import Optional

from docopt import docopt
from finalynx import Copilot
from finalynx import Dashboard
from finalynx import FetchFinary
from finalynx import Portfolio
from finalynx import Simulator
from rich import inspect  # noqa F401
from rich import pretty
from rich import print  # noqa F401
from rich import traceback
from rich.columns import Columns
from rich.panel import Panel

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
        scenario: Optional[Simulator] = None,
        copilot: Optional[Copilot] = None,
        ignore_orphans: bool = False,
        clear_cache: bool = False,
        force_signin: bool = False,
        hide_amounts: bool = False,
        hide_root: bool = False,
        show_data: bool = False,
        launch_dashboard: bool = False,
        output_format: str = "[console]",
    ):
        self.portfolio = portfolio
        self.scenario = scenario if scenario else Simulator()  # TODO Coming soon
        self.copilot = copilot if copilot else Copilot()  # TODO Coming soon

        # Options that can either be set in the constructor or from the command line
        self.ignore_orphans = ignore_orphans
        self.clear_cache = clear_cache
        self.force_signin = force_signin
        self.hide_amounts = hide_amounts
        self.hide_root = hide_root
        self.show_data = show_data
        self.launch_dashboard = launch_dashboard
        self.output_format = output_format

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
        simulation = self.scenario.rich_simulation(self.portfolio)  # noqa TODO

        # Get recommendations for immediate investment operations
        recommentations = self.copilot.rich_recommendations(self.portfolio)  # noqa TODO

        # Final set of results to be displayed
        panels = [
            Panel(
                self.portfolio.tree(
                    output_format=self.output_format,
                    hide_root=self.hide_root,
                    hide_amounts=self.hide_amounts,
                ),
                title=self.portfolio.name,
                padding=(1, 4),
            ),
            # Panel(simulation, title='Simulation'),   # TODO Coming soon
            # Panel(recommendations, title='Advisor'), # TODO Coming soon
        ]

        # Show the data fetched from Finary if specified
        if self.show_data:
            panels.append(Panel(finary_tree, title="Finary data"))

        # Display the entire portfolio and associated recommendations
        console.print("\n", Columns(panels, padding=(2, 10)))

        # Host a local webserver with the running dashboard
        if self.launch_dashboard:
            console.log("Launching dashboard.")
            Dashboard().run(portfolio=self.portfolio)
