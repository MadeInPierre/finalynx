import numpy as np
from .hierarchy import Hierarchy


class Target(Hierarchy):
    RESULT_NOK = {"name": "Not OK", "symbol": "×", "color": "red"}
    RESULT_OK = {"name": "OK", "symbol": "✓", "color": "green"}
    RESULT_TOLERATED = {"name": "Tolerated", "symbol": "≈", "color": "yellow"}
    RESULT_INVEST = {"name": "Invest", "symbol": "↗", "color": "red"}
    RESULT_DEVEST = {"name": "Devest", "symbol": "↘", "color": "magenta"}
    RESULT_START = {"name": "Start", "symbol": "↯", "color": "cyan"}
    RESULT_NONE = {"name": "No target", "symbol": "‣", "color": "blue"}

    def __init__(self, parent=None):
        super().__init__(parent)

    def get_amount(self):
        if self.parent is None:
            raise ValueError("[red]Target has no parent, not allowed.[/]")
        return self.parent.get_amount()

    def check(self):
        if self.get_amount() == 0:
            return Target.RESULT_START
        return Target.RESULT_NONE

    def prehint(self):
        return ""

    def hint(self):
        return (
            "- Gotta invest!" if self.check() == Target.RESULT_START else "- No target"
        )

    def render_amount(self, hide_amount=False, n_characters=0):
        result = self.check()
        result = (
            result if result != True else Target.RESULT_START
        )  # TODO weird bug??? Workaround for now
        number = (
            f"{round(self.get_amount()):>{n_characters}}" if not hide_amount else "···"
        )
        return f'[{result["color"]}]{result["symbol"]} {number} €[/][dim white]{self.prehint()}[/]'


class TargetRange(Target):
    def __init__(self, target_min, target_max, tolerance=0, parent=None):
        super().__init__(parent)
        self.target_min = target_min
        self.target_max = target_max
        self.tolerance = tolerance

    def check(self):
        if super_result := super().check() != Target.RESULT_NONE:
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

    def _get_variable(self):
        return self.get_amount()

    def hint(self):
        return f"- Range {self.target_min}-{self.target_max} €"


class TargetMax(TargetRange):
    def __init__(self, target_max, tolerance=0, parent=None):
        super().__init__(0, target_max, tolerance, parent)

    def hint(self):
        return f"- Maximum {self.target_max} €"


class TargetMin(TargetRange):
    def __init__(self, target_min, tolerance=0, parent=None):
        super().__init__(target_min, np.inf, tolerance, parent)

    def hint(self):
        return f"- Minimum {self.target_min} €"


class TargetRatio(TargetRange):
    def __init__(self, target_ratio, zone=4, tolerance=2, parent=None):
        target_min = max(target_ratio - zone, 0)
        target_max = min(target_ratio + zone, 100)
        super().__init__(target_min, target_max, tolerance, parent)
        self.target_ratio = target_ratio

    def get_ratio(self):
        total = self._get_reference_amount()
        return 100 * self.get_amount() / total if total > 0 else 0

    def _get_variable(self):
        return self.get_ratio()

    def _get_reference_amount(self):
        return self.parent.parent.get_amount()

    def prehint(self):
        return f" ({round(self.get_ratio()):>2}%)"

    def hint(self):
        return f"→ {self.target_ratio}%"


class TargetGlobalRatio(TargetRatio):
    def __init__(self, target_ratio, tolerance=0, parent=None):
        super().__init__(target_ratio, tolerance, parent)

    def _get_reference_amount(self):
        root = self.parent
        while root.parent is not None:
            root = root.parent
        return root.get_amount()

    def hint(self):
        return f"→ Global {self.target_ratio}%"
