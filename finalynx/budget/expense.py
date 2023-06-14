from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import List
from typing import Optional


class Status(Enum):
    UNKNOWN = "UNKNOWN"
    TODO = "TODO"
    DONE = "DONE"
    SKIP = "SKIP"


class Period(Enum):
    UNKNOWN = "UNKNOWN"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


class Constraint(Enum):
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

    def to_list(self) -> List[Any]:
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
        if not (4 <= len(list) <= 10):
            raise ValueError("List must have 4 to 10 elements, got", len(list))
        return Expense(
            timestamp=int(list[0]),
            amount=float(str(list[1]).replace("€", "").strip()),
            merchant_name=list[2],
            merchant_category=list[3],
            status=Status(list[4]) if list[4] else Status.UNKNOWN,
            i_paid=float(str(list[5]).replace("€", "").strip()) if list[5] else None,
            payback=list[6],
            constraint=Constraint(list[7]) if list[7] else Constraint.UNKNOWN,
            period=Period(list[8]) if list[8] else Period.UNKNOWN,
            comment=list[9],
            cell_number=cell_number,
        )
