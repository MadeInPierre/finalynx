from datetime import date
from typing import List
from typing import Optional

from finalynx.portfolio.folder import Portfolio
from finalynx.portfolio.line import Line
from finalynx.simulator.actions import Action
from finalynx.simulator.actions import AddLineAmount
from finalynx.simulator.recurrence import MonthlyRecurrence
from finalynx.simulator.recurrence import Recurrence


class Event:
    def __init__(
        self,
        action: Action,
        planned_date: Optional[date] = None,
        recurrence: Optional[Recurrence] = None,
        name: Optional[str] = None,
    ) -> None:
        """An event associates a date to an action."""
        self.name = name if name else action.name
        self.planned_date = planned_date if planned_date is not None else date.today()
        self.recurrence = recurrence
        self.action = action

    def apply(self, portfolio: Portfolio) -> List["Event"]:
        """Apply this event's consequence. This event can generate several new Events."""
        new_events = self.action.apply(portfolio)

        # Create a copy of this event with the new date if a recurrence is set
        if self.recurrence:
            if next_date := self.recurrence.next(self.planned_date):
                new_events.append(Event(self.action, next_date, self.recurrence, self.name))

        return new_events

    def __str__(self) -> str:
        return self.name


class Salary(Event):
    def __init__(
        self,
        target_line: Line,
        income: float,
        expenses: float = 0,
        day_of_the_month: int = 1,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        name: str = "Salary",
    ) -> None:
        super().__init__(
            AddLineAmount(target_line, income - expenses),
            start_date
            if start_date and start_date > date.today()
            else MonthlyRecurrence(day_of_the_month).next(date.today()),
            MonthlyRecurrence(day_of_the_month, until=end_date),
            name,
        )
