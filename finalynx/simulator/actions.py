from typing import Any
from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from finalynx.portfolio.bucket import Bucket
from finalynx.portfolio.folder import Folder
from finalynx.portfolio.folder import Portfolio
from finalynx.portfolio.folder import SharedFolder
from finalynx.portfolio.line import Line
from finalynx.portfolio.node import Node
from finalynx.portfolio.targets import TargetRatio

if TYPE_CHECKING:
    from finalynx.simulator.events import Event


class Action:
    """Abstract base class to perform an action on the portfolio."""

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
    """Set an amount to a line."""

    def __init__(self, target_line: Line, amount: float) -> None:
        """This action simply applies the new amount to the line. The timeline then processes
        the portfolio again to recalculate the SharedFolders' values.
        """
        self.target_line = target_line
        self.amount = amount
        super().__init__()

    def apply(self, portfolio: Portfolio) -> List["Event"]:
        self.target_line.amount = self.amount
        return []


class AddLineAmount(Action):
    """Add some amount to a line."""

    def __init__(self, target_line: Line, amount: float) -> None:
        """This action simply applies the new amount to the line. The timeline then processes
        the portfolio again to recalculate the SharedFolders' values.
        """
        self.target_line = target_line
        self.amount = amount
        super().__init__()

    def apply(self, portfolio: Portfolio) -> List["Event"]:
        self.target_line.amount += self.amount
        return []


class ApplyPerformance(Action):
    """Add the investment interests to each line (defined by the expected performance)."""

    def __init__(self, inflation: float = 2.0, period_years: float = 1.0) -> None:
        """This action applies every line's expected performance defined in `LinePerf`
        instances for the entire portfolio objecti.
        :param inflation: Float to reduce each line's performance by this number.
        :param period_years: Duration to apply the performance on. E.g. for one month, use 1/12.
        """
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
        # Timeline already processes the tree avec each event, no need here.
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


class AutoBalance(Action):
    """Automatically apply Finalynx's recommendations on the portfolio."""

    def apply(self, portfolio: Portfolio) -> List["Event"]:
        """This action automatically applies the ideal amounts auto-calculated
        in the portfolio tree. This only applies to `Line` and `SharedFolder`
        instances that have a `TargetRatio` target. The amounts are balanced
        depending on the target percentages for each node.
        Lines auto-added by envelope in folders are also balanced with equal
        percentages set for each child in the same folder.
        """
        ideals = self._get_ideals(portfolio)
        self._set_ideals(portfolio, ideals)
        return []

    def _get_ideals(self, node: Node) -> List[Any]:
        """Save the ideal amounts calculated in the tree before applying them to
        avoid inconsistent states."""
        if isinstance(node, Folder) and not isinstance(node, SharedFolder):
            return [self._get_ideals(c) for c in node.children]
        else:
            if (
                node.target.__class__.__name__ == "Target"
                and node.parent
                and isinstance(node.parent.target, TargetRatio)
            ):
                return [node.parent.get_ideal() / len(node.parent.children)]
            return [node.get_ideal()]

    def _set_ideals(self, node: Node, ideals: List[Any]) -> None:
        """Set the ideal amounts for each `Line` and `SharedFolder`."""

        # Traverse the tree to get to the leaves
        if isinstance(node, Folder) and not isinstance(node, SharedFolder):
            for i_child, child in enumerate(node.children):
                self._set_ideals(child, ideals[i_child])

        # At a leaf level, only update the amount if it's a node with a ratio target.
        # Add an exception for Lines auto-added in folders (no target set but the parent folder has a ratio)
        elif isinstance(node.target, TargetRatio) or (
            node.target.__class__.__name__ == "Target" and node.parent and isinstance(node.parent.target, TargetRatio)
        ):
            if isinstance(node, SharedFolder):
                node.bucket.add_amount(ideals[0] - node.get_amount())
            elif isinstance(node, Line):
                node.amount = ideals[0]
