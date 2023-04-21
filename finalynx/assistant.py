from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from docopt import docopt
from finalynx import Dashboard
from finalynx import FetchFinary
from finalynx import Portfolio
from finalynx.portfolio.envelope import Envelope
from finalynx.portfolio.folder import Folder
from finalynx.portfolio.folder import FolderDisplay
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
    ):
        self.portfolio = portfolio
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
        if args["targets"]:
            self.output_format = "[console_targets]"
            self.hide_deltas = True
        if args["text"]:
            self.output_format = "[text]"
            self.hide_deltas = True
        if args["--hide-deltas"]:
            self.hide_deltas = True

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
            Columns([Text("  ")] + render),  # type: ignore
            Panel(self.render_envelopes(), title="Envelope investments", padding=(1, 2), expand=False),
        ]

        # Show the data fetched from Finary if specified
        if self.show_data:
            panels.append(Panel(finary_tree, title="Finary data"))

        # Display the entire portfolio and associated recommendations
        console.print("\n", Columns(panels, padding=(2, 10)), "\n")

        # Host a local webserver with the running dashboard
        if self.launch_dashboard:
            console.log("Launching dashboard.")
            Dashboard().run(portfolio=self.portfolio)

    def render_envelopes(self) -> Tree:  # TODO missing deltas for folders as lines (e.g. ramify, or)
        """Sort lines with non-zero deltas by envelopes and display them as
        a summary of transfers to make."""
        tree = Tree("Envelopes", hide_root=True)

        for env in self.envelopes:
            children, env_delta = [], 0.0
            for line in env.lines:
                delta = line.get_delta()
                env_delta += delta
                if delta != 0 and line.target.check() not in [Target.RESULT_NONE, Target.RESULT_OK]:
                    children.append(line.render(output_format="[delta] [name]"))

            if children:
                env_delta = round(env_delta)
                render_delta = f"[{'green' if env_delta > 0 else 'red'}]{'+' if env_delta > 0 else ''}{env_delta} €"
                node = tree.add(f"{render_delta} [dodger_blue2 bold]{env.name}")
                for child in children:
                    node.add(child)
                node.children[-1].label += "\n"  # type: ignore

        def _get_collapsed_folders(node: Folder) -> List[Folder]:
            found = []
            for child in node.children:
                if isinstance(child, Folder):
                    if child.display == FolderDisplay.EXPANDED:
                        found += _get_collapsed_folders(child)
                    else:
                        found.append(child)
            return found

        node = tree.add("[dodger_blue2 bold]Collapsed folders")
        collapsed_folders = _get_collapsed_folders(self.portfolio)
        for f in collapsed_folders:
            if f.get_delta() != 0:
                node.add(f.render(output_format="[delta] [name]"))

        return tree
