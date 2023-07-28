from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from finalynx.portfolio.folder import Portfolio
from finalynx.portfolio.line import Line

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
