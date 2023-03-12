from typing import Optional
from typing import TYPE_CHECKING

from .node import Node

if TYPE_CHECKING:
    from .targets import Target
    from .folder import Folder


class Line(Node):
    def __init__(
        self,
        name: str,
        parent: Optional["Folder"] = None,
        target: Optional["Target"] = None,
        key: Optional[str] = None,
        amount: float = 0,
        newline: bool = False,
    ):
        super().__init__(name, parent, target, newline)
        self.key = key if key is not None else name
        self.amount = amount

    def get_amount(self) -> float:
        return self.amount
