from datetime import date
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from dateutil.relativedelta import relativedelta  # type: ignore

from .line import Line


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
        key: Optional[str] = None,
    ):
        self.name = name
        self.code = code
        self.date_created = date_created
        self.date_unlock = date_unlock if date_unlock else date_created
        self.date_untax = date_untax if date_untax else date_created
        self.key = key

        if not (self.date_created <= self.date_unlock <= self.date_untax):
            raise ValueError("Envelope dates must be ordered by created <= unlock <= untax")

        self.lines: List[Line] = []

    def link_line(self, line: Line) -> None:
        """Method used by Line objects so that this instance has a reference to its children"""
        self.lines.append(line)

    def get_state(self, date: date) -> EnvelopeState:
        """:return: The state of the envelope at the specified `date` based on the instance's
        creation, unlock, and untax dates."""
        if date < self.date_created:
            return EnvelopeState.CLOSED
        elif date < self.date_unlock:
            return EnvelopeState.LOCKED
        elif date < self.date_untax:
            return EnvelopeState.TAXED
        else:
            return EnvelopeState.FREE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "code": self.code,
            "date_created": self.date_created.isoformat(),
            "date_unlock": self.date_unlock.isoformat(),
            "date_untax": self.date_untax.isoformat(),
        }

    @staticmethod
    def from_dict(dict: Dict[str, Any]) -> "Envelope":
        return Envelope(
            dict["name"],
            dict["code"],
            date.fromisoformat(dict["date_created"]),
            date.fromisoformat(dict["date_unlock"]),
            date.fromisoformat(dict["date_untax"]),
        )


class PEA(Envelope):
    def __init__(self, name: str, code: str, date_created: date, key: Optional[str] = None):
        date_unlock = date_created + relativedelta(years=5)
        super().__init__(name, code, date_created, date_unlock, date_unlock, key=key)


class PEE(Envelope):
    def __init__(
        self, name: str, code: str, date_created: date, date_unlock: Optional[date] = None, key: Optional[str] = None
    ):
        if not date_unlock:
            date_unlock = date_created + relativedelta(years=5)
        super().__init__(name, code, date_created, date_unlock, date_unlock, key=key)


class AV(Envelope):
    def __init__(self, name: str, code: str, date_created: date, key: Optional[str] = None):
        date_untax = date_created + relativedelta(years=8)
        super().__init__(name, code, date_created, date_created, date_untax, key=key)


class PER(Envelope):
    def __init__(self, name: str, code: str, date_created: date, date_retirement: date, key: Optional[str] = None):
        super().__init__(name, code, date_created, date_retirement, date_retirement, key=key)
