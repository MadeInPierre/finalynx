from typing import Callable
from typing import Dict
from typing import Optional
from typing import TYPE_CHECKING

from .constants import AssetClass
from .node import Node

if TYPE_CHECKING:
    from .envelope import Envelope
    from .targets import Target
    from .folder import Folder


class Line(Node):
    """This class represents a single investment line in your online account (e.g. Finary)."""

    def __init__(
        self,
        name: str,
        asset_class: AssetClass = AssetClass.UNKNOWN,
        parent: Optional["Folder"] = None,
        target: Optional["Target"] = None,
        key: Optional[str] = None,
        amount: float = 0,
        newline: bool = False,
        envelope: Optional["Envelope"] = None,
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
        # Setup custom aliases for node rendering
        render_agents: Dict[str, Callable[..., str]] = {
            "account_code": self._render_account_code,
        }

        super().__init__(name, parent, target, newline, agents=render_agents)
        self.asset_class = asset_class
        self.key = key if key is not None else name
        self.amount = amount
        self.envelope = envelope

        # Let the envelope know that this is a child line
        if self.envelope:
            self.envelope.link_line(self)

    def get_amount(self) -> float:
        """:returns: The amount invested in this line."""
        return self.amount

    def _render_account_code(self) -> str:
        return f"[{self.envelope.code}] " if self.envelope else ""
