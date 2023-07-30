from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import TYPE_CHECKING

import numpy as np

from ..config import DEFAULT_CURRENCY
from ..config import get_active_theme as TH
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
        perf: Optional[LinePerf] = None,
        currency: Optional[str] = None,
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

        super().__init__(
            name,
            asset_class,
            asset_subclass,
            parent,
            target,
            newline,
            perf if perf else LinePerf(0),
            currency,
            envelope,
            agents=render_agents,
        )
        self.key = key if key is not None else name
        self.amount = amount

        # Let the envelope know that this is a child line
        if self.envelope:
            self.envelope.link_line(self)

    def get_amount(self) -> float:
        """:returns: The amount invested in this line."""
        return self.amount

    def get_perf(self) -> LinePerf:
        """:returns: The expected yearly performance of this line (set by user)."""
        assert self.perf is not None
        return self.perf

    def apply_perf(self, inflation: float = 2.0, n_years: float = 1.0) -> float:
        """Applies the performance if set. `n_years` specifies the period to apply
        the performance over (e.g. 1 / 12 = 0.0833 for one month).
        :returns: The gained amount, or None if no perf was defined."""
        if self.perf is None or (self.perf is not None and self.perf.skip):
            return np.nan
        percentage = (self.perf.expected - inflation) / (100 * n_years)
        gain = self.get_amount() * percentage
        self.amount += gain
        return gain

    def _render_account_code(self) -> str:
        """:returns: A formatted string representation of this line's envelope."""
        return f"[{TH().ENVELOPE_CODE}][{self.envelope.code}][/] " if self.envelope else ""

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

    def copy(self) -> "Line":
        return Line(
            name=self.name,
            asset_class=self.asset_class,
            asset_subclass=self.asset_subclass,
            parent=self.parent,
            target=self.target,
            key=self.key,
            amount=self.amount,
            newline=self.newline,
            perf=self.perf,
            currency=self.currency,
            envelope=self.envelope,
        )
