"""
Finary Assistant command line
Usage:
    your_config.py [-iarf]
    your_config.py (-h | --help)
    your_config.py (-v | --version)

Options:
  -h --help           Show this help message
  -v --version        Display this module's current version
  -i --ignoreOrphans  Ignore fetched lines that you didn't reference in your portfolio
  -f --forceSignin    Sign in to Finary even if there is an existing cookies file
  -a --hideAmount     Display your portfolio with dots instead of the real values (easier to share)
  -r --hideRoot       Display your portfolio without the root (cosmetic preference)

"""
from finary_assistant import Copilot, Simulator, finary_fetch, console, __version__
from docopt import docopt

# Enable rich's features
from rich import print, inspect, pretty, traceback
from rich.columns import Columns
from rich.text import Text
from rich.panel import Panel

traceback.install()
pretty.install()


class Assistant:
    """
    Main entry class. Declare your portfolio config (and other extensions
    such as scenario and copilot) in a separate file and create an instance
    of this Assistant class.

    TODO Full code documentation! Ping me if I still didn't write it :)
    """

    def __init__(
        self,
        portfolio,
        scenario=None,
        copilot=None,
        ignore_orphans=False,
        force_signin=False,
        hide_amount=False,
        hide_root=False,
    ):
        self.portfolio = portfolio
        self.scenario = scenario if scenario else Simulator()  # TODO Coming soon
        self.copilot = copilot if copilot else Copilot()  # TODO Coming soon

        # Options
        self.ignore_orphans = ignore_orphans
        self.force_signin = force_signin
        self.hide_amount = hide_amount
        self.hide_root = hide_root

        self.parse_args()

    def parse_args(self):
        args = docopt(__doc__, version=__version__)
        if args["--ignoreOrphans"]:
            self.ignore_orphans = True
        if args["--forceSignin"]:
            self.force_signin = True
        if args["--hideAmount"]:
            self.hide_amount = True
        if args["--hideRoot"]:
            self.hide_root = True

    def run(self):
        # Fill tree with current valuations fetched from Finary
        finary_tree = finary_fetch(self.portfolio, self.force_signin, self.ignore_orphans)

        # Mandatory step after fetching to process some targets and buckets
        self.portfolio.process()

        # Simulate the portolio's evolution through the years by auto-investing each month
        simulation = self.scenario.rich_simulation(self.portfolio)

        # Get recommendations for immediate investment operations
        recommentations = self.copilot.rich_recommendations(self.portfolio)

        # Final set of results to be displayed
        panels = [
            Panel(
                self.portfolio.rich_tree(
                    hide_amount=self.hide_amount, hide_root=self.hide_root
                ),
                title=self.portfolio.name,
                padding=(1, 4),
            ),
            Panel(finary_tree, title="Finary data"),
            # Panel(simulation, title='Simulation'),   # TODO Coming soon
            # Panel(recommendations, title='Advisor'), # TODO Coming soon
        ]

        # Display the entire portfolio and associated recommendations
        console.print("\n", Columns(panels, padding=(2, 10)))
