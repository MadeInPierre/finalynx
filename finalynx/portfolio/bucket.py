import copy
import itertools
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import TYPE_CHECKING

import numpy as np

from .constants import AssetClass
from .folder import Folder
from .folder import FolderDisplay
from .line import Line

if TYPE_CHECKING:
    from .targets import Target


class Bucket:
    """
    Holds a list of `Line` objects to represent a group of investments that hold the same purpose.

    Once defined with a list of lines, there is nothing else to do from a user perspective.
    The user can reference this bucket instance in as many `SharedFolder` instances in the
    portfolio tree as desired. Each folder will only user the specified `target_amount` in
    each folder instance, and the bucket will generate a new list of liens for this folder
    with only the specified amount, while keeping track of what has been already used.
    """

    def __init__(self, lines: List["Line"]):
        self.lines = [] if lines is None else lines
        self._prev_amount_used: float = 0
        self.amount_used: float = 0

    def get_max_amount(self) -> float:
        return float(np.sum([line.get_amount() for line in self.lines]))

    def _get_cumulative_index(self, target: float) -> Dict[str, Any]:
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
        result_prev = self._get_cumulative_index(self._prev_amount_used)
        result = self._get_cumulative_index(self.amount_used)
        sublines = []

        if result["index"] == result_prev["index"]:
            new_line = copy.deepcopy(self.lines[result["index"]])
            new_line.amount = result["remainder"] - result_prev["remainder"]
            sublines.append(new_line)
        else:
            line1 = copy.deepcopy(self.lines[result_prev["index"]])
            line1.amount = line1.amount - result_prev["remainder"]
            sublines.append(line1)

            for i in range(result_prev["index"] + 1, result["index"]):
                sublines.append(copy.deepcopy(self.lines[i]))

            line2 = copy.deepcopy(self.lines[result["index"]])
            line2.amount = result["remainder"]
            sublines.append(line2)

        return sublines

    def use_amount(self, amount: float) -> List["Line"]:
        self._prev_amount_used = self.amount_used
        self.amount_used = min(self.get_max_amount(), self.amount_used + amount)
        return self.get_lines()

    def get_used_amount(self) -> float:
        return self.amount_used


class SharedFolder(Folder):
    def __init__(
        self,
        name: str,
        bucket: Bucket,
        asset_class: AssetClass = AssetClass.UNKNOWN,
        target_amount: float = np.inf,
        parent: Optional["Folder"] = None,
        target: Optional["Target"] = None,
        newline: bool = False,
        display: FolderDisplay = FolderDisplay.EXPANDED,
    ):
        super().__init__(name, asset_class, parent, target, bucket.lines, newline=False, display=display)  # type: ignore # TODO couldn't fix the mypy error
        self.target_amount = target_amount
        self.newline = newline
        self.bucket = bucket

    def process(self) -> None:
        super().process()  # Process children
        self.children = self.bucket.use_amount(self.target_amount)  # type: ignore # TODO couldn't fix the mypy error

        for child in self.children:
            child.set_parent(self)

        if self.children:
            self.children[-1].newline = self.newline

    def set_child_amount(self, key: str, amount: float) -> bool:
        """Used by the `fetch` subpackage to

        This method passes down the vey:value pair corresponding to an investment fetched online
        (e.g. in your Finary account) to its children until a match is found.

        :param key: Name of the line in the online account.
        :param amount: Fetched amount in the online account.
        """
        success = False
        for child in self.children:
            if isinstance(child, Line) and child.key == key:
                child.amount = amount
                success = True
            elif isinstance(child, Folder) and child.set_child_amount(key, amount):
                success = True
        return success
