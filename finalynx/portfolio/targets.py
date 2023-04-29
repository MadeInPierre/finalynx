from typing import Any
from typing import Dict
from typing import TYPE_CHECKING

import numpy as np

from .hierarchy import Hierarchy

if TYPE_CHECKING:
    from .node import Node


class Target(Hierarchy):
    """Abstract class that defines an objective for a `Node` in the Portfolio tree."""

    RESULT_NOK = {"name": "NOK", "symbol": "×", "color": "red"}
    RESULT_OK = {"name": "OK", "symbol": "✓", "color": "green"}
    RESULT_TOLERATED = {"name": "Tolerated", "symbol": "≈", "color": "yellow"}
    RESULT_INVEST = {"name": "Invest", "symbol": "↗", "color": "red"}
    RESULT_DEVEST = {"name": "Devest", "symbol": "↘", "color": "magenta"}
    RESULT_START = {"name": "Start", "symbol": "↯", "color": "cyan"}
    RESULT_NONE = {"name": "No target", "symbol": "‣", "color": "black"}

    def __init__(self) -> None:
        """Abstract Target class that holds the Node parent using this instance and provides
        a common logic for rendering the amounts."""
        super().__init__(parent=None)
        self.parent: Node = self.parent  # Tell mypy this class only has Nodes as parents.

    def get_amount(self) -> float:
        """:returns: The amount stored in the target's parent."""
        if self.parent is None:
            raise ValueError("[red]Target has no parent, not allowed.[/]")
        return self.parent.get_amount()

    def get_ideal(self) -> float:
        """:returns: The ideal amount to be invested based on surrounding targets."""
        return 0.0

    def check(self) -> Dict[str, str]:
        """Default behavior to check if the parent's amount respects the target objective.
        This method should be overriden by all subclasses to define custom-tailored logic.
        :returns: A `Target.RESULT_*` object depending on the recommendation to be rendered
        in the output console.
        """
        if self.get_amount() == 0:
            return Target.RESULT_START
        return Target.RESULT_NONE

    def prehint(self) -> str:
        """Virtual method for information to be printed between the amoutn and the name."""
        return ""

    def hint(self) -> str:
        """Virtual method for information to be printed at the end of the parent's description."""
        return "- Invest!" if self.check() == Target.RESULT_START else ""

    def render_amount(self, hide_amount: bool = False, n_characters: int = 0) -> str:
        """Check for the parent's amount against the target logic and format the amount based on the target recommendation.
        :param hide_amount: Replace the amounts by simple dots (easier to share the result), defaults to False.
        :param n_characters: Used by `Node` objects to align the amount with other nodes' renders.
        :returns: A string with a righ-formatted render of the parent's amount based on the target recommendation.
        """
        result = self.check()
        result = result if result != True else Target.RESULT_START  # type: ignore # noqa: E712 TODO weird bug??? Workaround for now
        number = f"{round(self.get_amount()):>{n_characters}}" if not hide_amount else "···"
        return (
            f'[{result["color"]}]{result["symbol"]} {number} {self._render_currency()}[/][dim white]{self.prehint()}[/]'
        )

    def render_ideal(self) -> str:
        """Ideal amount to be reached based on the current target and node
        position in the tree. Must be overridden by subclasses."""
        return ""

    def render_goal(self) -> str:
        """Ideal amount or ratio to be reached based on the current target and node
        position in the tree. Must be overridden by subclasses."""
        return ""

    def _render_target_name(self) -> str:
        """:returns: The name of the target recommentation."""
        return self.check()["name"]

    def _render_target_symbol(self) -> str:
        """:returns: The UFT-8 symbol associated to the target recommentation."""
        return self.check()["symbol"]

    def _render_target_color(self) -> str:
        """:returns: The color associated to the target recommentation."""
        return self.check()["color"]

    def _render_currency(self) -> str:
        """:returns: This parent's currency symbol, used for target render methods."""
        if not self.parent:
            raise ValueError("Target's parent must not be None.")
        return self.parent._render_currency()

    def to_dict(self) -> Dict[str, Any]:
        """Empty dict, should be overridden by subclasses."""
        return {}

    @staticmethod
    def from_dict(dict: Dict[str, Any]) -> "Target":
        if "type" not in dict:
            return Target()
        elif dict["type"] == "range":
            return TargetRange(dict["target_min"], dict["target_max"], dict["tolerance"])
        elif dict["type"] == "max":
            return TargetMax(dict["target_max"], dict["tolerance"])
        elif dict["type"] == "min":
            return TargetMin(dict["target_min"], dict["tolerance"])
        elif dict["type"] == "ratio":
            return TargetRatio(dict["target_ratio"], dict["zone"], dict["tolerance"])
        elif dict["type"] == "global_ratio":
            return TargetGlobalRatio(dict["target_ratio"], dict["zone"], dict["tolerance"])
        else:
            raise ValueError("Unrecognized target type.")


class TargetRange(Target):
    """Target to make sure your node stays within a specified range."""

    def __init__(self, target_min: float, target_max: float, tolerance: float = 0):
        """This target checks if the amount is between two values (with an optional tolerance).
        :param target_min: Minimum threshold to get a `RESULT_OK`.
        :param target_max: Maximum threshold to get a `RESULT_OK`.
        :param tolerance: If the amount is between `target_min - tolerance` and `target_max + tolerance`,
        the check will return a `RESULT_TOLERATED`.
        """
        super().__init__()
        self.target_min = target_min
        self.target_max = target_max
        self.tolerance = tolerance

    def check(self) -> Dict[str, str]:
        """This function checks the conditions described in the init method."""
        super_result = super().check()
        if super_result != Target.RESULT_NONE:
            return super_result
        elif self._get_variable() < self.target_min - self.tolerance:
            return Target.RESULT_INVEST
        elif self._get_variable() < self.target_min:
            return Target.RESULT_TOLERATED
        elif self._get_variable() <= self.target_max:
            return Target.RESULT_OK
        elif self._get_variable() <= self.target_max + self.tolerance:
            return Target.RESULT_TOLERATED
        return Target.RESULT_DEVEST

    def get_ideal(self) -> float:
        """:returns: The ideal amount to be invested based on surrounding targets."""
        if self.target_min <= self.get_amount() <= self.target_max:
            return self.get_amount()
        elif self.get_amount() < self.target_min:
            return self.target_min
        return self.target_max

    def render_ideal(self) -> str:
        """:returns: The average between target boundaries."""
        return f"{round(self.get_ideal())} {self._render_currency()} "

    def render_goal(self) -> str:
        """:returns: Same as ideal amount."""
        return f"{round(self.get_ideal())} {self._render_currency()} "

    def _get_variable(self) -> float:
        """Internal method that gives the value to be checked (overriden by subclasses)."""
        return self.get_amount()

    def hint(self) -> str:
        """:returns: A formatted description of the target."""
        return f"- Range {self.target_min}-{self.target_max} {self._render_currency()}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "range",
            "target_min": self.target_min,
            "target_max": self.target_max,
            "tolerance": self.tolerance,
        }


class TargetMax(TargetRange):
    """Target to make sure your node does not exceed a specified value."""

    def __init__(self, target_max: float, tolerance: float = 0):
        """This target checks if the amount is below a specified threshold (with an optional tolerance).
        :param target_max: Maximum threshold to get a `RESULT_OK`.
        :param tolerance: If the amount is at most `target_max + tolerance`, the check will return a `RESULT_TOLERATED`.
        """
        super().__init__(0, target_max, tolerance)

    def get_ideal(self) -> float:
        """:returns: The ideal amount to be invested based on surrounding targets."""
        return self.target_max

    def hint(self) -> str:
        """:returns: A formatted description of the target."""
        return f"- Maximum {self.target_max} {self._render_currency()}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "max",
            "target_max": self.target_max,
            "tolerance": self.tolerance,
        }


class TargetMin(TargetRange):
    """Target to make sure your node does not go under a specified value."""

    def __init__(self, target_min: float, tolerance: float = 0):
        """This target checks if the amount is above a specified threshold (with an optional tolerance).
        :param target_min: Minimum threshold to get a `RESULT_OK`.
        :param tolerance: If the amount is at least `target_min - tolerance`, the check will return a `RESULT_TOLERATED`.
        """
        super().__init__(target_min, np.inf, tolerance)

    def get_ideal(self) -> float:
        """:returns: The ideal amount to be invested based on surrounding targets."""
        return self.target_min

    def hint(self) -> str:
        """:returns: A formatted description of the target."""
        return f"- Minimum {self.target_min} {self._render_currency()}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "min",
            "target_min": self.target_min,
            "tolerance": self.tolerance,
        }


class TargetRatio(TargetRange):
    """Target to make sure your node represents a specified ratio in a folder."""

    def __init__(self, target_ratio: float, zone: float = 4, tolerance: float = 2):
        """This target checks if the amount represents a specified ratio of the total amounf of the parent node
        (with an optional tolerance).
        :param target_ratio: Target to get a `RESULT_OK`.
        :param zone: Accepted tolerance to still return a `RESULT_OK`.
        :param tolerance: If the amount is between `target_ratio - (zone + tolerance) / 2` and `target_ratio + (zone + tolerance) / 2`,
        the check will return a `RESULT_TOLERATED`.
        """
        target_min = max(target_ratio - zone, 0)
        target_max = min(target_ratio + zone, 100)
        super().__init__(target_min, target_max, tolerance)
        self.target_ratio = target_ratio
        self.zone = zone

    def get_ratio(self) -> float:
        """:returns: How much this amount represents agains the reference in percentage (0-100%)."""
        total = self._get_reference_amount()
        return 100 * self.get_amount() / total if total > 0 else 0

    def get_ideal(self) -> int:
        """:returns: How much this amount represents agains the reference in percentage (0-100%)."""
        return round(self._get_reference_amount() * self.target_ratio / 100)

    def render_goal(self) -> str:
        """:returns: The target ratio as a string."""
        return f"{self.target_ratio:>2} % "

    def _get_variable(self) -> float:
        """:returns: The value to be checked."""
        return self.get_ratio()

    def _get_reference_amount(self) -> float:
        """:returns: The value to be checked against (parent's amount)."""
        if not self.parent.parent:
            raise ValueError("Target's parent's parent must not be None.")

        # If the parent also has a ratio target, propagate the reference amount
        if isinstance(self.parent.parent.target, TargetRatio):
            return self.parent.parent.target.get_ideal()

        # Otherwise, simply get the parent's value
        return self.parent.parent.get_amount()

    def prehint(self) -> str:
        """:returns: A rich-formatted view of the calculated percentage."""
        if not self.parent or not self.parent.parent:
            raise ValueError("Target's parent must be set.")

        max_length = 0
        for child in self.parent.parent.children:
            if isinstance(child.target, TargetRatio):
                max_length = max(max_length, len(str(round(child.target.get_ideal()))))

        return f"→ {self.get_ideal():>{max_length}} {self._render_currency()}"

    def hint(self) -> str:
        """:returns: A formatted description of the target."""
        return f"{round(self.get_ratio())}% → {self.target_ratio}%"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "ratio",
            "target_ratio": self.target_ratio,
            "zone": self.zone,
            "tolerance": self.tolerance,
        }


class TargetGlobalRatio(TargetRatio):
    """Target to make sure your node represents a specified ratio in your portfolio."""

    def __init__(self, target_ratio: float, zone: float = 4, tolerance: float = 0):
        """This target checks if the amount represents a specified ratio of the total amount of your entire portfolio.
        :param target_ratio: Target to get a `RESULT_OK`.
        :param zone: Accepted tolerance to still return a `RESULT_OK`.
        :param tolerance: If the amount is between `target_ratio - (zone + tolerance) / 2` and `target_ratio + (zone + tolerance) / 2`,
        the check will return a `RESULT_TOLERATED`.
        """
        super().__init__(target_ratio, zone, tolerance)

    def _get_reference_amount(self) -> float:
        """:returns: The value to be checked against (portfolio amount)."""
        root = self.parent
        while root.parent is not None:
            root = root.parent
        return root.get_amount()

    def hint(self) -> str:
        """:returns: A formatted description of the target."""
        return f"Global {round(self.get_ratio())}% → {self.target_ratio}%"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "global_ratio",
            "target_ratio": self.target_ratio,
            "zone": self.zone,
            "tolerance": self.tolerance,
        }
