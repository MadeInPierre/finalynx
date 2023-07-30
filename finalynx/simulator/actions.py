from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from finalynx.portfolio.bucket import Bucket
from finalynx.portfolio.folder import Folder
from finalynx.portfolio.folder import Portfolio
from finalynx.portfolio.folder import SharedFolder
from finalynx.portfolio.line import Line
from finalynx.portfolio.node import Node

if TYPE_CHECKING:
    from finalynx.simulator.events import Event


class Action:
    def __init__(self, name: Optional[str] = None) -> None:
        """Abstract class. An action describes a procedure to change something in the portfolio.
        For instance, when receiving a salary, an action could add some amount to the main account.
        """
        self.name = name if name else self.__class__.__name__

    def apply(self, portfolio: Portfolio) -> List["Event"]:
        """Apply this action's consequence, must be overridden."""
        raise NotImplementedError("Must be overridden.")

    def __str__(self) -> str:
        return self.name


class SetLineAmount(Action):
    def __init__(self, target_line: Line, amount: float) -> None:
        self.target_line = target_line
        self.amount = amount
        super().__init__()

    def apply(self, portfolio: Portfolio) -> List["Event"]:
        self.target_line.amount = self.amount
        return []


class AddLineAmount(Action):
    def __init__(self, target_line: Line, amount: float) -> None:
        self.target_line = target_line
        self.amount = amount
        super().__init__()

    def apply(self, portfolio: Portfolio) -> List["Event"]:
        self.target_line.amount += self.amount
        return []


class ApplyPerformance(Action):
    def __init__(self, inflation: float = 2.0, period_years: float = 1.0) -> None:
        self.period_years = period_years
        self.inflation = inflation
        super().__init__()
        self._buckets: List[Bucket] = []

    def apply(self, portfolio: Portfolio) -> List["Event"]:
        """Applies the performance if set. `n_years` specifies the period to apply
        the performance over (e.g. 1 / 12 = 0.0833 for one month).
        :returns: The gained amount, or None if no perf was defined."""

        # Apply the performance for each Line in the tree
        self._buckets.clear()
        self._apply_perf(portfolio)

        # Collect the buckets in the tree, apply the performance for each of
        # their lines, and process again to redistribute the new amounts.
        for bucket in set(self._buckets):
            for line in bucket.lines:
                line.apply_perf(self.inflation, self.period_years)

        return []

    def _apply_perf(self, node: Node) -> None:
        """Traverse the tree, apply the performance for Lines, and collect the buckets for use later."""
        if isinstance(node, SharedFolder):
            self._buckets.append(node.bucket)
        elif isinstance(node, Folder):
            for c in node.children:
                self._apply_perf(c)
        elif isinstance(node, Line):
            node.apply_perf(self.inflation, self.period_years)
        else:
            raise ValueError("Unexpected node type.")
