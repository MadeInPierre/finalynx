from datetime import date
from enum import Enum
from typing import List
from typing import Optional

from dateutil.relativedelta import relativedelta
from finalynx.portfolio.line import Line


class EnvelopeState(Enum):
    UNKNOWN = "Unknown"
    CLOSED = "Closed"
    LOCKED = "Locked"
    TAXED = "Taxed"
    FREE = "Free"


class Envelope:
    def __init__(
        self,
        name: str,
        code: str,
        date_created: date,
        date_unlock: Optional[date] = None,
        date_untax: Optional[date] = None,
    ):
        self.name = name
        self.code = code
        self.date_created = date_created
        self.date_unlock = date_unlock if date_unlock else date_created
        self.date_untax = date_untax if date_untax else date_created

        if not (self.date_created <= self.date_unlock <= self.date_untax):
            raise ValueError("Envelope dates must be ordered by created <= unlock <= untax")

        self.lines: List[Line] = []

    def link_line(self, line: Line) -> None:
        """Method used by Line objects so that this instance has a reference to its children"""
        self.lines.append(line)

    def get_state(self, date: date) -> EnvelopeState:
        if date < self.date_created:
            return EnvelopeState.CLOSED
        elif date < self.date_unlock:
            return EnvelopeState.LOCKED
        elif date < self.date_untax:
            return EnvelopeState.TAXED
        else:
            return EnvelopeState.FREE


class PEA(Envelope):
    def __init__(self, name: str, code: str, date_created: date):
        date_unlock = date_created + relativedelta(years=5)
        super().__init__(name, code, date_created, date_unlock, date_unlock)


class AV(Envelope):
    def __init__(self, name: str, code: str, date_created: date):
        date_untax = date_created + relativedelta(years=8)
        super().__init__(name, code, date_created, date_created, date_untax)


class PER(Envelope):
    def __init__(self, name: str, code: str, date_created: date, date_retirement: date):
        super().__init__(name, code, date_created, date_retirement, date_retirement)
