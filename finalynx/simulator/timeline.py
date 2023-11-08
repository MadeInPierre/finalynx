from dataclasses import dataclass
from datetime import date
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from finalynx.analyzer.investment_state import AnalyzeInvestmentStates
from finalynx.portfolio.bucket import Bucket
from finalynx.portfolio.envelope import EnvelopeState
from finalynx.portfolio.folder import Portfolio
from finalynx.simulator.actions import AutoBalance
from finalynx.simulator.events import Event
from finalynx.simulator.events import YearlyPerformance
from finalynx.simulator.recurrence import MonthlyRecurrence


@dataclass
class Simulation:
    """Configuration class to launch a Finalynx simulation."""

    # List of events to execute
    events: Optional[List[Event]] = None

    # Inflation rate to apply to the portfolio every year (used if default events are enabled)
    inflation: float = 2.0

    # Simulation end date, if None the simulation will run for 100 years
    end_date: Optional[date] = None

    # Whether to pre-add common default events (yearly performance, auto-balance, etc.)
    default_events: bool = True

    # Whether to print the final portfolio state in the console after the simulation
    print_final: bool = False

    # Whether to print the final portfolio state in the console after the simulation
    print_each_step: bool = False
    
    # Display the portfolio's worth in the console every `step` years
    step_years: int = 5


class Timeline:
    """Main simulation engine to execute programmed actions on your portfolio."""

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
        self._events = simulation.events if simulation.events else []

        # Create default events in addition to the user ones and sort events by date
        if simulation.default_events:
            self._events += [
                YearlyPerformance(simulation.inflation),
                Event(AutoBalance(), recurrence=MonthlyRecurrence(1, n_months=3)),
            ]
        self._sort_events()

        # This is a pointer to the current portfolio's date, which will move when applying events
        self.current_date = date.today()
        self.end_date = simulation.end_date if simulation.end_date else date.today() + timedelta(weeks=100 * 52)

        # Log some metrics during the simulation to display them at the end
        self._log_dates: List[date] = []  # Dates at which the portfolio metrics were logged
        self._log_env_states: Dict[str, List[float]] = {c.value: [] for c in EnvelopeState}

    def run(self) -> None:
        """Step all events until the simulation limit is reached."""
        self.goto(self.end_date)

    def goto(self, target_date: date) -> None:
        """Step until the target date is reached (in the future or past)."""
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

        # Record the metrics if the year changed
        if next_event.planned_date.year != self.current_date.year:
            self._record_metrics()

        # Move the current date to this event's date
        self.current_date = next_event.planned_date
        return False

    def unstep_until(self, target_date: date) -> None:
        """Undo all events until the specified date is reached."""
        raise NotImplementedError("Cannot unstep yet.")

    def unstep(self) -> None:
        """Undo the last event and go back to the previous date."""
        raise NotImplementedError("Cannot unstep yet.")

    @property
    def is_finished(self) -> bool:
        """The timeline is finished if there are no events left to step
        or the limit date is reached."""
        return len(self._events) == 0 or self.current_date >= self.end_date

    def _record_metrics(self) -> None:
        """Record the portfolio's metrics at the current date to display later."""
        self._log_dates.append(self.current_date)

        # Record the envelope states and their amounts at this date
        for key, value in AnalyzeInvestmentStates(self._portfolio).analyze(self.current_date).items():
            self._log_env_states[key].append(value)

    def chart(self) -> Dict[str, Any]:
        """Plot a Highcharts chart of the portfolio's envelopes' states and amounts over time."""
        assert self._log_env_states, "Run the simulation before charting."

        colors = {
            "Unknown": "#434348",
            "Closed": "#999999",
            "Locked": "#F94144",
            "Taxed": "#F9C74F",
            "Free": "#7BB151",
        }

        return {
            "chart": {"plotBackgroundColor": None, "plotBorderWidth": None, "plotShadow": False, "type": "area"},
            "title": {"text": "Simulation", "align": "center"},
            "plotOptions": {
                "series": {"pointStart": self._log_dates[0].year},
                "area": {
                    "stacking": "normal",
                    "lineColor": "#666666",
                    "lineWidth": 1,
                    "marker": {"lineWidth": 1, "lineColor": "#666666", "enabled": False},
                },
            },
            "series": [
                {
                    "name": key,
                    "data": value,
                    "color": colors[key],
                }
                for key, value in self._log_env_states.items()
            ],
            "credits": {"enabled": False},
        }

    def _sort_events(self) -> None:
        """Internal method to sort the event list by planned date."""
        self._events.sort(key=lambda event: event.planned_date)

    def __str__(self) -> str:
        return f"Timeline at {self.current_date}"
