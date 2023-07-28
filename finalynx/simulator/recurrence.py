from datetime import date
from datetime import timedelta
from typing import Optional


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
