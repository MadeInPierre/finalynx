from datetime import date
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from dateutil.relativedelta import relativedelta  # type: ignore

from .line import Line


class EnvelopeState(Enum):
    """Depending on the date, an envelope can be at a certain state
    (locked, heavily taxed, free, etc)."""

    UNKNOWN = "Unknown"
    CLOSED = "Closed"
    LOCKED = "Locked"
    TAXED = "Taxed"
    FREE = "Free"


class Envelope:
    """Represents an investment envelope or account (e.g. PEA, Assurance Vie, ...)."""

    def __init__(
        self,
        name: str,
        code: str,
        date_created: date,
        date_unlock: Optional[date] = None,
        date_untax: Optional[date] = None,
        key: Optional[str] = None,
    ):
        """
        This class represents any investment envelope or account (e.g. PEA, Assurance Vie, CTO, ...)
        and can be used to

        :param name: The envelope name (can also act as the `key` if the key is not set), will be
        displayed in the console and webdashboard
        :param code: The envelope name in a short version (recommended 3 characters), will be displayed
        when rendering each line to indicate each line's envelope.
        :param date_created: Accepts a `date` object to indicate when this envelope was opened.
        :param date_unlock: Accepts a `date` object to indicate when this envelope will be unlocked. For
        instance, a PEA will be unlocked 5 years after creation as required by law.
        :param date_untax: Accepts a `date` object to indicate when this envelope will no longer have
        higher-than-usual tax rates. For instance, a French Assurance Vie is highly taxed for the first
        8 years after creation date, and then changes to a better tax rate.
        :param key: If you want to set a different name here from Finary's name, set the Finary name in
        this `key` parameter. The field `name` will be used when displaying the envelope in Finalynx.
        """
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
    """Handy shortcut to quickly define a PEA (automatically sets 5-years locked)."""

    def __init__(self, name: str, code: str, date_created: date, key: Optional[str] = None):
        """Declare a PEA (locked for 5 years) with:
        :param name: Name of your account.
        :param code: Short name of your account (3 characters recommended).
        :param date_created: A `date` instance of the account creation date.
        :param key: Optional, if you want to use a different name in Finalynx than in Finary.
        See `Envelope`'s documentation for additional details.
        """
        date_unlock = date_created + relativedelta(years=5)
        super().__init__(name, code, date_created, date_unlock, date_unlock, key=key)


class PEE(Envelope):
    """Handy shortcut to quickly define a PEE (automatically sets 5-years locked)."""

    def __init__(
        self, name: str, code: str, date_created: date, date_unlock: Optional[date] = None, key: Optional[str] = None
    ):
        """Declare a PEE (locked for 5 years) with:
        :param name: Name of your account.
        :param code: Short name of your account (3 characters recommended).
        :param date_created: A `date` instance of the account creation date.
        :param date_unlock: A `date` instance of the account unlock date, defaults to 5 years.
        :param key: Optional, if you want to use a different name in Finalynx than in Finary.
        See `Envelope`'s documentation for additional details.
        """
        if not date_unlock:
            date_unlock = date_created + relativedelta(years=5)
        super().__init__(name, code, date_created, date_unlock, date_unlock, key=key)


class AV(Envelope):
    """Handy shortcut to quickly define a PEA (automatically sets 8-years taxed)."""

    def __init__(self, name: str, code: str, date_created: date, key: Optional[str] = None):
        """Declare an Assurance Vie (taxed for 8 years) with:
        :param name: Name of your account.
        :param code: Short name of your account (3 characters recommended).
        :param date_created: A `date` instance of the account creation date.
        :param key: Optional, if you want to use a different name in Finalynx than in Finary.
        See `Envelope`'s documentation for additional details.
        """
        date_untax = date_created + relativedelta(years=8)
        super().__init__(name, code, date_created, date_created, date_untax, key=key)


class PER(Envelope):
    """Handy shortcut to quickly define a PER (locked until retirement)."""

    def __init__(self, name: str, code: str, date_created: date, date_retirement: date, key: Optional[str] = None):
        """Declare a PER (locked until retirement) with:
        :param name: Name of your account.
        :param code: Short name of your account (3 characters recommended).
        :param date_created: A `date` instance of the account creation date.
        :param date_retirement: A `date` instance of your expected retirement date.
        :param key: Optional, if you want to use a different name in Finalynx than in Finary.
        See `Envelope`'s documentation for additional details.
        """
        super().__init__(name, code, date_created, date_retirement, date_retirement, key=key)
