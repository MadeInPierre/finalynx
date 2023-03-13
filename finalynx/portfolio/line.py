from typing import Optional
from typing import TYPE_CHECKING

from .node import Node

if TYPE_CHECKING:
    from .targets import Target
    from .folder import Folder


class Line(Node):
    """This class represents a single investment line in your online account (e.g. Finary)."""

    def __init__(
        self,
        name: str,
        parent: Optional["Folder"] = None,
        target: Optional["Target"] = None,
        key: Optional[str] = None,
        amount: float = 0,
        newline: bool = False,
    ):
        """
        This is a subclass of `Node` that adds an `amount` and `key` property.

        :param name: The name that will be displayed in the final portfolio tree.
        :param parent: Parent of this line. If this line is created in a `Folder` instance,
        the folder will set iself as the parent at the initialization stage.
        :param target: Optional `Target` instance to format this line's amount based on the objective you selected.
        :param key: Optional string that must be identical to the name in the online account
        (e.g. Finary). Defaults to the `name` if the key is not set.
        :param amount: How much has been invested on this investment line. If you connect your online
        account, the amount you specify will be replaced by what has been fetched online.
        :param newline: Print a new line in the console at the end of this `Line` for better readability.
        """
        super().__init__(name, parent, target, newline)
        self.key = key if key is not None else name
        self.amount = amount

    def get_amount(self) -> float:
        """:returns: The amount invested in this line."""
        return self.amount
