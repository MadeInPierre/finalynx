# Enable rich's features
from rich import print, inspect, pretty, traceback
from rich.columns import Columns
from rich.text import Text
from rich.panel import Panel
traceback.install()
pretty.install()

# # Fetch imports
from finary_assistant import Copilot, Simulator
from finary_assistant import finary_fetch
from finary_assistant import console


class Assistant:
    def __init__(self, portfolio, scenario=None, copilot=None, 
        ignore_orphans=False, 
        hide_amount=False,
        hide_root=False):
        self.portfolio = portfolio
        self.scenario = scenario if scenario else Simulator() # TODO Coming soon
        self.copilot = copilot if copilot else Copilot()      # TODO Coming soon

        # Options
        self.ignore_orphans = ignore_orphans
        self.hide_amount = hide_amount
        self.hide_root = hide_root
    
    def parse_args(self, args):
        print('TODO') # TODO

    def run(self):
        # Fill tree with current valuations fetched from Finary
        with console.status('[bold green]Fetching data from Finary...'):
            finary_tree = finary_fetch(self.portfolio, self.ignore_orphans)
        
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
                    hide_amount=self.hide_amount, 
                    hide_root=self.hide_root
                ), 
                title=self.portfolio.name, 
                padding=(1, 4)
            ), 
            Panel(finary_tree, title='Finary data'),
            # Panel(simulation, title='Simulation'),   # TODO Coming soon
            # Panel(recommendations, title='Advisor'), # TODO Coming soon
        ]

        # Display the entire portfolio and associated recommendations
        console.print('\n', Columns(panels, padding=(2, 10)))