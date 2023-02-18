import numpy as np
from .folder import Folder, FolderDisplay
from .line import Line
from ..console import console
import itertools
import copy


class Bucket:
    def __init__(self, lines=None):
        self.lines = [] if lines is None else lines
        self._prev_amount_used = 0
        self.amount_used = 0

    def get_max_amount(self):
        return np.sum([l.get_amount() for l in self.lines])

    def _get_cumulative_index(self, target):
        result = {"index": -1, "remainder": 0}
        amounts = [l.get_amount() for l in self.lines]
        cumulative_sum = list(itertools.accumulate(amounts))
        for i, item in enumerate(cumulative_sum):
            if item >= target:
                result["index"] = i
                result["remainder"] = target - (cumulative_sum[i - 1] if i != 0 else 0)
                return result

    def get_lines(self):
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

    def use_amount(self, amount):
        self._prev_amount_used = self.amount_used
        self.amount_used = min(self.get_max_amount(), self.amount_used + amount)
        return self.get_lines()

    def get_used_amount(self):
        return self.amount_used

    def get_free_amount(self):
        return self.get_amount() - self.get_used_amount()


class SharedFolder(Folder):
    def __init__(
        self,
        name,
        bucket,
        target_amount=np.inf,
        parent=None,
        target=None,
        newline=False,
        display=FolderDisplay.EXPANDED,
    ):
        super().__init__(
            name, parent, target, bucket.lines, newline=False, display=display
        )
        self.target_amount = target_amount
        self.newline = newline
        self.bucket = bucket

    def process(self):
        super().process()  # Process children
        self.children = self.bucket.use_amount(self.target_amount)

        for child in self.children:
            child.set_parent(self)

        if self.children:
            self.children[-1].newline = self.newline
