from datetime import date
from typing import List
from typing import Optional

from finalynx.portfolio.folder import Portfolio
from finalynx.portfolio.line import Line
from finalynx.simulator.actions import Action
from finalynx.simulator.actions import AddLineAmount
from finalynx.simulator.actions import ApplyPerformance
from finalynx.simulator.recurrence import DeltaRecurrence
from finalynx.simulator.recurrence import MonthlyRecurrence
from finalynx.simulator.recurrence import RecurrenceBase


class Event:
    """Program an action to happen at a certain (optionally recurring) date."""

    def __init__(
        self,
        action: Action,
        planned_date: Optional[date] = None,
        recurrence: Optional[RecurrenceBase] = None,
        name: Optional[str] = None,
    ) -> None:
        """An event associates a date to an action.
        :param action: `Action` instance to execute.
        :param planned_date: Date when the action should be executed.
        :param recurrence: Optional recurrence to repeat the action every month/year/other.
        :param name: Optional name of the event, defaults to the action's name.
        """
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
    """Add your salary to your account every month (nicer shortcut)."""

    def __init__(
        self,
        target_line: Line,
        income: float,
        expenses: float = 0,
        day_of_the_month: int = 1,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        income_growth: float = 0,
        expenses_follow: float = 0,
        name: str = "Salary",
    ) -> None:
        """Add your salary to your account every month (nicer shortcut). The salary amount can
        grow with a fixed percentage every year. The expenses can follow the income gains with a
        fixed percentage every year (0 means every new gain is invested, 100 means every gain is
        used to increase your way of life).

        :param target_line: `Line` reference in the portfolio to add the salary to.
        :param income: Monthly salary amount.
        :param expenses: Monthly expenses amount.
        :param day_of_the_month: Day of the month to add the salary to the portfolio.
        :param start_date: When to start adding the salary to the portfolio, defaults to today's next month.
        :param end_date: When to stop adding the salary to the portfolio, defaults to no end date.
        :param income_growth: Annual salary growth rate.
        :param expenses_follow: Annual expenses growth rate (percentage of income gains reinvested).
        :param name: Name of the event.
        """
        self.target_line = target_line
        self.day_of_the_month = day_of_the_month
        self.start_date = start_date

        self.income = income
        self.expenses = expenses
        self.income_growth = income_growth
        self.expenses_follow = expenses_follow

        super().__init__(
            AddLineAmount(target_line, income - expenses),
            start_date
            if start_date and start_date > date.today()
            else MonthlyRecurrence(day_of_the_month).next(date.today()),
            MonthlyRecurrence(day_of_the_month, until=end_date),
            name,
        )

    def apply(self, portfolio: Portfolio) -> List["Event"]:
        """Update the salary amount with the growth rates. Creates a new salary
        with the updated income/expense amounts depending on the growth rates."""
        self.action.apply(portfolio)

        assert self.recurrence is not None  # Needed for mypy
        if next_date := self.recurrence.next(self.planned_date):
            income_gains = self.income * self.income_growth / (12 * 100)
            return [
                Salary(
                    target_line=self.target_line,
                    income=self.income + income_gains,
                    expenses=self.expenses + income_gains * self.expenses_follow / 100,
                    day_of_the_month=self.day_of_the_month,
                    start_date=next_date,
                    end_date=self.recurrence.until,
                    income_growth=self.income_growth,
                    expenses_follow=self.expenses_follow,
                    name=self.name,
                )
            ]
        return []


class YearlyPerformance(Event):
    """Earn your investments' interests at the end of each year."""

    def __init__(
        self,
        inflation: float,
        start_year: Optional[int] = None,
        repeat_annual: bool = True,
        name: str = "Yearly Performance",
    ) -> None:
        start_date = date(start_year if start_year is not None else date.today().year, 12, 31)
        recurrence = DeltaRecurrence(years=1) if repeat_annual else None
        super().__init__(ApplyPerformance(inflation), start_date, recurrence, name)
