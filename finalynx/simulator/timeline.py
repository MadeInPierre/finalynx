from dataclasses import dataclass
from datetime import date
from datetime import timedelta
from typing import List
from typing import Optional

from finalynx.portfolio.bucket import Bucket
from finalynx.portfolio.folder import Portfolio
from finalynx.simulator.events import Event
from finalynx.simulator.events import YearlyPerformance


@dataclass
class Simulation:
    events: List[Event]
    inflation: float = 2.0
    end_date: Optional[date] = None
    default_events: bool = True


class Timeline:
    def __init__(
        self,
        simulation: Simulation,
        portfolio: Portfolio,
        buckets: List[Bucket],
    ) -> None:
        """The timeline is a list of programmed events. The user can set his own list of events
        with optional recurring settings. The timeline will automatically apply each event and
        generate the recurring events until `duration_years` is reached."""
        self.simulation = simulation
        self._portfolio = portfolio
        self._buckets = buckets

        # Create default events, add the user ones, and sort by date
        self._events = simulation.events
        if simulation.default_events:
            self._events += [
                YearlyPerformance(simulation.inflation),
                # TODO auto-balance the portfolio by following the recommendations
            ]
        self._sort_events()

        # This is a pointer to the current portfolio's date, which will move when applying events
        self.current_date = date.today()
        self.end_date = simulation.end_date if simulation.end_date else date.today() + timedelta(weeks=100 * 52)

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
