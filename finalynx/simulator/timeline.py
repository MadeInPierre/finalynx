from datetime import date
from datetime import timedelta
from typing import List
from typing import Optional

from finalynx import Portfolio
from finalynx.portfolio.bucket import Bucket
from finalynx.portfolio.line import Line


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


class Recurrence:
    def __init__(self, until: Optional[date] = None) -> None:
        self.until = until

    def next(self, current_date: date) -> Optional[date]:
        next_date = self._next_date(current_date)
        if self.until and next_date > self.until:
            return None
        return next_date

    def _next_date(self, current_date: date) -> date:
        raise NotImplementedError("Must be overridden by subclass.")


class DeltaRecurrence(Recurrence):
    def __init__(
        self,
        days: Optional[int] = None,
        months: Optional[int] = None,
        years: Optional[int] = None,
        until: Optional[date] = None,
    ) -> None:
        super().__init__(until)
        assert days is not None or months is not None or years is not None, "Set at least one time field"

        days = days if days is not None else 0
        months = months if months is not None else 0
        years = years if years is not None else 0

        self._delta = timedelta(days, weeks=4 * months + 52 * years)

    def _next_date(self, current_date: date) -> date:
        return current_date + self._delta


class MonthlyRecurrence(Recurrence):
    def __init__(
        self,
        day_of_the_month: int,
        until: Optional[date] = None,
    ) -> None:
        super().__init__(until)
        self.day_of_the_month = day_of_the_month

    def _next_date(self, current_date: date) -> date:
        if current_date.month == 12:
            return date(current_date.year + 1, 1, self.day_of_the_month)
        return date(current_date.year, current_date.month + 1, self.day_of_the_month)


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


class Timeline:
    def __init__(
        self,
        portfolio: Portfolio,
        buckets: List[Bucket],
        events: List[Event],
        end_date: Optional[date] = None,
    ) -> None:
        """The timeline is a list of programmed events. The user can set his own list of events
        with optional recurring settings. The timeline will automatically apply each event and
        generate the recurring events until `duration_years` is reached."""
        self._portfolio = portfolio
        self._buckets = buckets
        self._events = events
        self._sort_events()

        # This is a pointer to the current portfolio's date, which will move when applying events
        self.current_date = date.today()
        self.end_date = end_date if end_date else date.today() + timedelta(weeks=100 * 52)

    def run(self) -> None:
        self.goto(self.end_date)

    def goto(self, target_date: date) -> None:
        """"""
        if target_date == self.current_date:
            return
        elif target_date > self.current_date:
            self.step_until(target_date)
        else:
            self.unstep_until(target_date)
        self.current_date = target_date

    def step_until(self, target_date: date) -> None:
        """Execute all events until the specified date is reached."""
        assert self.current_date < target_date, "Target date must be in the future."

        while self.current_date < target_date and not self.is_finished:
            if self.step():
                return

    def step(self) -> bool:
        """Execute the next event. This may generate new events in the stack.
        :returns: True if the simulation ended (no more events)."""
        if self.is_finished:
            return True

        # State check
        next_event = self._events[0]
        assert self.current_date <= next_event.planned_date, "Cannot step into a past event."
        if next_event.planned_date >= self.end_date:
            return True

        # Add the newly generated events and sort the event list by date
        new_events = next_event.apply(self._portfolio)

        # Recalculate the amounts for shared folders
        for bucket in self._buckets:
            bucket.reset()
        self._portfolio.process()

        # TODO auto-balance the portfolio by following the recommendations
        # TODO apply the yearly performance for each Line in the portfolio
        # TODO apply inflation (inside the performance or after?)

        # Remove this event, add the new ones, and sort by date
        self._events.remove(next_event)
        self._events += new_events
        self._sort_events()

        # Move the current date to this event's date
        self.current_date = next_event.planned_date
        # console.log(
        #     f"{next_event.planned_date} Portfolio has "
        #     f"{round(self._portfolio.get_amount())} € after event {next_event}"
        # )
        return False

    def unstep_until(self, target_date: date) -> None:
        """Undo all events until the specified date is reached."""
        raise NotImplementedError("Cannot unstep yet.")

    def unstep(self) -> None:
        """Undo the last event and go back to the previous date."""
        raise NotImplementedError("Cannot unstep yet.")

    @property
    def is_finished(self) -> bool:
        return len(self._events) == 0 or self.current_date >= self.end_date

    def _sort_events(self) -> None:
        """Internal method to sort the event list by planned date."""
        self._events.sort(key=lambda event: event.planned_date)

    def __str__(self) -> str:
        return f"Timeline at {self.current_date}"


"""
if __name__ == "__main__":
    from rich import print

    line = Line("My Line", amount=1500)
    portfolio = Portfolio(children=[line])

    print(portfolio.tree())

    t = Timeline(
        portfolio,
        [],
        [
            # Event(SetLineAmount(line, 1000), date(2023, 8, 27), DeltaRecurrence(months=1, until=date(2025, 1, 1))),
            # Event(SetLineAmount(line, 1000), date(2023, 8, 27), MonthlyRecurrence(3, until=date(2024, 1, 1))),
            # Event(AddLineAmount(line, 1000), date(2023, 8, 27), MonthlyRecurrence(3, until=date(2024, 1, 1))),
            # Event(AddLineAmount(line, 1000), recurrence=MonthlyRecurrence(3)),
            Salary(line, 2500, 1500, end_date=date(2024, 11, 30), name="Salaire Stellantis"),
            Event(AddLineAmount(line, 4000), planned_date=date(2024, 4, 10), name="Prime Stellantis"),
            Event(AddLineAmount(line, 3500), planned_date=date(2025, 4, 10), name="Prime Stellantis"),
            Salary(line, 3500, 2000, start_date=date(2025, 1, 1)),
        ],
        end_date=date(1998 + 65, 4, 5),
    )

    t.run()
    print(portfolio.tree())

    print("\n======\nFinished!")
    print(t)
    print(line.render())
"""
