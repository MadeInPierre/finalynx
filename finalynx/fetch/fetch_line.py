"""This file defines elements used to match `Line` instances defined in the main portfolio
tree with investments fetched online (e.g. from your Finary account).
"""
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Optional

from finalynx.config import DEFAULT_CURRENCY
from finalynx.portfolio.line import Line


@dataclass
class FetchAttribs:
    """Abstract class that defines common attributes used to match Keys (defined in the portfolio)
    with FetchLines (created by fetch agents, e.g. `FinaryFetch`)."""

    name: Optional[str] = None
    id: Optional[str] = None
    account: Optional[str] = None
    custom: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        """Runs after an instance is created to validate inputs. At least one field must be set."""
        if not (self.name or self.id or self.account or self.custom):
            raise ValueError(f"{type(self).__name__} instance must have at least one field set.")

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @staticmethod
    def from_dict(dict: Dict[str, Any]) -> "FetchAttribs":
        raise NotImplementedError("Abstract method must be overridden by subclasses.")


@dataclass
class FetchLine(FetchAttribs):
    """Represents each investment found in your online accounts (e.g. Finary). The instance is
    populated with information found online about this line. FetchLines will then be matched to Keys
    defined in the portfolio to populate 'real' `Line` instances with FetchLine information."""

    amount: float = 0
    currency: Optional[str] = None

    def matches_line(self, line: Line) -> bool:  # TODO improve?
        # See if the line's name or key fields match
        matched_name = bool((line.key and line.key in [self.name, self.id, self.account]) or line.name == self.name)

        # If the envelope is set, it must also match
        if line.envelope:
            return matched_name and (line.envelope.name == self.account or line.envelope.key == self.account)

        # If there's no envelope set, only the name/key counts
        return matched_name

    def update_line(self, line: Line) -> None:
        """Update a `Line` instance, usually matched against a FetchKe, in the portfolio,
        with data fetched online."""
        if not line.amount:
            line.amount = self.amount
        if not line.currency:
            line.currency = self.currency if self.currency else DEFAULT_CURRENCY

    def generate_line(self) -> Line:
        """Generate a basic Line instance from this abstract fetched line.
        Used when filling folders based on account filters."""
        name = self.name if self.name else "Unknown"
        return Line(name, key=self.id, amount=self.amount, currency=self.currency)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @staticmethod
    def from_dict(dict: Dict[str, Any]) -> "FetchLine":
        return FetchLine(
            name=dict["name"],
            id=dict["id"],
            account=dict["account"],
            custom=dict["custom"],
            amount=dict["amount"],
            currency=dict["currency"],
        )
