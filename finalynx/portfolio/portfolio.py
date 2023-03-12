from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from .folder import Folder


if TYPE_CHECKING:
    from .node import Node
    from .targets import Target


class Portfolio(Folder):
    def __init__(
        self, name: str = "Portfolio", target: Optional["Target"] = None, children: Optional[List["Node"]] = None
    ):
        super().__init__(name, parent=None, target=target, children=children, newline=False)
