from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import pytz


class Status(Enum):
    UNKNOWN = "UNKNOWN"
    TODO = "TODO"
    DONE = "DONE"
    SKIP = "SKIP"


class Period(Enum):
    UNKNOWN = "UNKNOWN"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


class Constraint(Enum):  # TODO rename to Necessity
    UNKNOWN = "UNKNOWN"
    FIXED = "FIXED"
    MODULAR = "MODULAR"
    NOCHOICE = "NOCHOICE"
    VARIABLE = "VARIABLE"
    OPTIONAL = "OPTIONAL"
    HOBBIES = "HOBBIES"
    FUN = "FUN"


@dataclass
class Expense:
    # Information from N26 and/or manual input
    timestamp: int
    amount: float
    merchant_name: str
    merchant_category: str

    # Information from user input to manage the status
    status: Status = Status.UNKNOWN
    i_paid: Optional[float] = None
    payback: str = ""
    constraint: Constraint = Constraint.UNKNOWN
    period: Period = Period.UNKNOWN
    comment: str = ""

    # Internal information
    cell_number: int = -1

    def as_datetime(self, timezone: str = "Europe/Paris") -> datetime:
        """Return the timestamp as a datetime object in the given timezone."""
        return (
            datetime.utcfromtimestamp(int(self.timestamp) / 1000)
            .replace(tzinfo=pytz.UTC)
            .astimezone(pytz.timezone(timezone))
        )

    def to_list(self) -> List[Any]:
        """Return the expense as a list of values. Used for Google Sheets export/import."""
        return [
            int(self.timestamp),
            float(self.amount),
            str(self.merchant_name),
            str(self.merchant_category),
            str(self.status.value) if self.status != Status.UNKNOWN else "",
            float(self.i_paid) if self.i_paid is not None else "",
            str(self.payback),
            str(self.constraint.value) if self.constraint != Constraint.UNKNOWN else "",
            str(self.period.value) if self.period != Period.UNKNOWN else "",
            str(self.comment),
        ]

    @staticmethod
    def from_list(list: List[Any], cell_number: int = -1) -> "Expense":
        """Create an Expense object from a list of values. Used for Google Sheets export/import."""
        if len(list) < 4:
            raise ValueError("List must have at least 4 elements, got", len(list))
        return Expense(
            timestamp=int(list[0]),
            amount=float(str(list[1]).replace("€", "").replace(",", "").strip()),
            merchant_name=list[2],
            merchant_category=list[3],
            status=Status(list[4]) if list[4] else Status.UNKNOWN,
            i_paid=float(str(list[5]).replace("€", "").replace(",", "").strip()) if list[5] else None,
            payback=list[6],
            constraint=Constraint(list[7]) if list[7] else Constraint.UNKNOWN,
            period=Period(list[8]) if list[8] else Period.UNKNOWN,
            comment=list[9],
            cell_number=cell_number,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return the expense as a dictionary. Used for JSON export/import."""
        return {
            "timestamp": str(self.timestamp),
            "amount": str(self.amount),
            "merchant_name": self.merchant_name,
            "merchant_category": self.merchant_category,
            "status": self.status.value,
            "i_paid": str(self.i_paid),
            "payback": self.payback,
            "constraint": self.constraint.value,
            "period": self.period.value,
            "comment": self.comment,
            "cell_number": str(self.cell_number),
        }

    @staticmethod
    def from_dict(dict_: Dict[str, Any]) -> "Expense":
        """Create an Expense object from a dictionary. Used for JSON export/import."""
        return Expense(
            timestamp=int(dict_["timestamp"]),
            amount=float(str(dict_["amount"]).replace("€", "").strip()),
            merchant_name=dict_["merchant_name"],
            merchant_category=dict_["merchant_category"],
            status=Status(dict_["status"]) if dict_["status"] else Status.UNKNOWN,
            i_paid=float(str(dict_["i_paid"]).replace("€", "").strip()) if dict_["i_paid"] != "None" else None,
            payback=dict_["payback"],
            constraint=Constraint(dict_["constraint"]) if dict_["constraint"] else Constraint.UNKNOWN,
            period=Period(dict_["period"]) if dict_["period"] else Period.UNKNOWN,
            comment=dict_["comment"],
            cell_number=int(dict_["cell_number"]),
        )
