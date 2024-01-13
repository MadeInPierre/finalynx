from datetime import date
from datetime import timedelta
from typing import Optional


class RecurrenceBase:
    """Abstract class to define how often an Event should be triggered."""

    def __init__(self, until: Optional[date] = None) -> None:
        self.until = until

    def next(self, current_date: date) -> Optional[date]:
        next_date = self._next_date(current_date)
        if self.until and next_date > self.until:
            return None
        return next_date

    def _next_date(self, current_date: date) -> date:
        raise NotImplementedError("Must be overridden by subclass.")


class DeltaRecurrence(RecurrenceBase):
    """Program an action to happen every few days/months/years."""

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

        # Add decimals to stay on the same day (otherwise Yearly goes to 30/12)
        self._delta = timedelta(days, weeks=4.3452 * months + 52.1429 * years + 0.1429)

    def _next_date(self, current_date: date) -> date:
        return current_date + self._delta


class MonthlyRecurrence(RecurrenceBase):
    """Program an action to happen every nth day of the month."""

    def __init__(
        self,
        day_of_the_month: int,
        n_months: int = 1,
        until: Optional[date] = None,
    ) -> None:
        """Program an action to happen every nth day of the month.
        :param n_months: Optionally skip some months.
        """
        super().__init__(until)
        self.day_of_the_month = day_of_the_month
        self.n_months = n_months

    def _next_date(self, current_date: date) -> date:
        next_month = current_date.month + self.n_months

        if next_month > 12:
            return date(current_date.year + 1, next_month - 12, self.day_of_the_month)
        return date(current_date.year, next_month, self.day_of_the_month)
