"""
```{tip}
% TODO
These enumerations are not yet used in Finalynx, but will serve as the basis for the `Analyzer`
subpackage to classify lines and show relevant statistics.
```
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class LinePerf:
    """Represents a Line's expected performance.
    :param expected: this investment's expected yearly return (e.g. 2 for 2%/yr)
    :param skip: Don't use this line when calculating the performance in upper nodes
    """

    expected: float
    pessimistic: Optional[float] = 0  # TODO not used
    optimistic: Optional[float] = 0  # TODO not used
    skip: bool = False

    @staticmethod
    def from_dict(dict: Dict[str, Any]) -> "LinePerf":
        return LinePerf(expected=dict["expected"], skip=dict["skip"])


class AssetClass(Enum):
    """Enumeration that defines the asset class for each line."""

    CASH = "Cash"
    LIVRET = "Livrets"
    FOND_EURO = "Fonds euro"
    BOND = "Obligations"
    STOCK = "Actions"
    REAL_ESTATE = "Immobilier"
    GOLD = "Or"
    CRYPTO = "Cryptos"
    PASSIVE = "Passifs"
    UNKNOWN = "Inconnu"


class EnvelopeClass(Enum):  # TODO use or remove?
    """Enumeration that defines the envelope types that hold each line."""

    CCP = "CCP"
    LIVRET = "Livret"
    AV = "AV"
    PEA = "PEA"
    CTO = "CTO"
    PER = "PER"
    WALLET = "Wallet"
    PLATFORM = "Plateforme"
    PHYSICAL = "Physique"
    PASSIVE = "Passif"
