import itertools
from typing import Any
from typing import Dict
from typing import List
from typing import TYPE_CHECKING

import numpy as np

from .line import Line

if TYPE_CHECKING:
    from .envelope import Envelope


class Bucket:
    """
    Holds a list of `Line` objects to represent a group of investments that hold the same purpose.

    Once defined with a list of lines, there is nothing else to do from a user perspective.
    The user can reference this bucket instance in as many `SharedFolder` instances in the
    portfolio tree as desired. Each folder will only user the specified `target_amount` in
    each folder instance, and the bucket will generate a new list of liens for this folder
    with only the specified amount, while keeping track of what has been already used.
    """

    def __init__(self, name: str, lines: List["Line"]):
        """:param name: Name for the bucket used to display it and export it to JSON.
        :param lines: List of `Line` instances that will be shared with all `SharedFolder` objects
        that use this `Bucket`.
        """
        self.name = name
        self.lines = [] if lines is None else lines
        self._prev_amount_used: float = 0
        self.amount_used: float = 0

    def get_max_amount(self) -> float:
        """:returns: The total amount contained in this bucket."""
        return float(np.sum([line.get_amount() for line in self.lines]))

    def _get_cumulative_index(self, target: float) -> Dict[str, Any]:
        """:returns: A dictionary containing the Line index where the cumulative sum meets,
        and the remainder amount not used in this line."""
        result = {"index": -1, "remainder": 0.0}
        amounts = [line.get_amount() for line in self.lines]
        cumulative_sum = list(itertools.accumulate(amounts))
        for i, item in enumerate(cumulative_sum):
            if item >= target:
                result["index"] = i
                result["remainder"] = target - (cumulative_sum[i - 1] if i != 0 else 0)
                return result
        return result

    def get_lines(self) -> List["Line"]:
        """:returns: A copy of the `Bucket`'s lines between the two previous `use_amount()`
        calls."""
        result_prev = self._get_cumulative_index(self._prev_amount_used)
        result = self._get_cumulative_index(self.amount_used)
        sublines = []

        if result["index"] == result_prev["index"]:
            new_line = self.lines[result["index"]].copy()
            new_line.amount = result["remainder"] - result_prev["remainder"]
            sublines.append(new_line)
        else:
            line1 = self.lines[result_prev["index"]].copy()
            line1.amount = line1.amount - result_prev["remainder"]
            sublines.append(line1)

            for i in range(result_prev["index"] + 1, result["index"]):
                sublines.append(self.lines[i].copy())

            line2 = self.lines[result["index"]].copy()
            line2.amount = result["remainder"]
            sublines.append(line2)

        return sublines

    def use_amount(self, amount: float) -> List["Line"]:
        """Ask to consume the specified amount from the bucket.
        :returns: A list of copies of the used Lines with their respective used amounts.
        Next time this method is called, the bucket will start from the cumulative amount
        used so far."""
        self._prev_amount_used = self.amount_used
        self.amount_used = min(self.get_max_amount(), self.amount_used + amount)
        return self.get_lines()

    def get_used_amount(self) -> float:
        """:return: The total amount used from the bucket until now."""
        return self.amount_used

    def add_amount(self, amount: float) -> None:
        """Add or remove an amount to the bucket's lines. This can be used to dynamically change the
        bucket's total amount, e.g. to apply recommendations from Finalynx during the simulation"""

        # If the amount is positive, add the amount to the last line in the bucket
        if amount > 0:
            if not self.lines:
                raise ValueError("Cannot add amount to an empty bucket.")
            self.lines[-1].amount += amount

        # If the amount is negative, remove successively from each line
        else:
            amount *= -1
            removed_amount = 0.0
            for line in reversed(self.lines):
                remaining_amount = amount - removed_amount

                if line.amount >= remaining_amount:
                    line.amount -= remaining_amount
                    return
                else:
                    removed_amount += line.amount
                    line.amount = 0

        raise ValueError("Attempted to remove too much from the bucket.")

    def reset(self) -> None:
        """Go back to a state where no amount was used."""
        self._prev_amount_used = 0
        self.amount_used = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "lines": [line.to_dict() for line in self.lines],
        }

    @staticmethod
    def from_dict(dict: Dict[str, Any], envelopes: Dict[str, "Envelope"]) -> "Bucket":
        return Bucket(dict["name"], [Line.from_dict(line, envelopes) for line in dict["lines"]])
