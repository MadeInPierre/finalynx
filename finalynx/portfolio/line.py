from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import TYPE_CHECKING

from ..config import DEFAULT_CURRENCY
from .constants import AssetClass
from .constants import AssetSubclass
from .constants import LinePerf
from .node import Node
from .targets import Target

if TYPE_CHECKING:
    from .envelope import Envelope
    from .folder import Folder


class Line(Node):
    """This class represents a single investment line in your online account (e.g. Finary)."""

    def __init__(
        self,
        name: str,
        asset_class: AssetClass = AssetClass.UNKNOWN,
        asset_subclass: AssetSubclass = AssetSubclass.UNKNOWN,
        parent: Optional["Folder"] = None,
        target: Optional["Target"] = None,
        key: Optional[str] = None,
        amount: float = 0,
        newline: bool = False,
        envelope: Optional["Envelope"] = None,
        perf: Optional[LinePerf] = None,
        currency: Optional[str] = None,
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

        super().__init__(name, parent, target, newline, agents=render_agents, currency=currency)
        self.asset_class = asset_class
        self.asset_subclass = asset_subclass
        self.key = key if key is not None else name
        self.amount = amount
        self.envelope = envelope
        self.perf = perf if perf else LinePerf(0)

        # Let the envelope know that this is a child line
        if self.envelope:
            self.envelope.link_line(self)

    def get_amount(self) -> float:
        """:returns: The amount invested in this line."""
        return self.amount

    def get_perf(self) -> LinePerf:
        """:returns: The expected yearly performance of this line (set by user)."""
        return self.perf

    def _render_account_code(self) -> str:
        """:returns: A formatted string representation of this line's envelope."""
        return f"[{self.envelope.code}] " if self.envelope else ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "line",
            "name": self.name,
            "asset_class": self.asset_class.value,
            "asset_subclass": self.asset_subclass.value,
            "key": self.key,
            "amount": self.amount,
            "target": self.target.to_dict(),
            "envelope_name": self.envelope.name if self.envelope else "",
            "perf": self.perf.__dict__,
            "newline": self.newline,
            "currency": self.currency,
        }

    @staticmethod
    def from_dict(dict: Dict[str, Any], envelopes: Dict[str, "Envelope"]) -> "Line":
        return Line(
            name=dict["name"],
            asset_class=AssetClass(dict["asset_class"]),
            asset_subclass=AssetSubclass(dict["asset_subclass"])
            if "asset_subclass" in dict.keys()
            else AssetSubclass.UNKNOWN,
            key=dict["key"],
            amount=dict["amount"],
            target=Target.from_dict(dict["target"]),
            envelope=envelopes[dict["envelope_name"]] if dict["envelope_name"] else None,
            perf=LinePerf.from_dict(dict["perf"]),
            newline=bool(dict["newline"]),
            currency=dict["currency"] if "currency" in dict.keys() else DEFAULT_CURRENCY,
        )
