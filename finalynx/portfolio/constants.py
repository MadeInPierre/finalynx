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
    GUARANTEED = "Garanti"
    BOND = "Obligations"
    STOCK = "Actions"
    REAL_ESTATE = "Immobilier"
    MATERIAL = "Métaux"
    CRYPTO = "Cryptos"
    PASSIVE = "Passifs"
    EXOTIC = "Exotiques"
    UNKNOWN = "Inconnu"
    DIVERSIFIED = "Diversifié"


class AssetSubclass(Enum):
    """Default collection of assets used as asset subclasses (for easier visualization and analysis)."""

    # Cash
    CASH_CCP = "Comptes courants"
    CASH_MONETARY = "Monétaire"

    # Guaranteed investments (mostly french)
    GUARANTEED_LIVRET = "Livrets"
    GUARANTEED_LIVRET_TAXED = "Livrets imposables"
    GUARANTEED_FOND_EURO = "Fonds euro"

    # Bonds
    BOND_DATED = "Fonds datés"
    BOND_ETF = "ETFs Obligations"

    # Stocks
    STOCK_SHARE = "Titres vifs"
    STOCK_ETF = "ETFs Actions"

    # Real estate
    REAL_ESTATE_PHYSICAL = "Immobilier physique"
    REAL_ESTATE_SCPI = "SCPI"
    REAL_ESTATE_SCI = "SCI"

    # Metals
    MATERIAL_GOLD = "Or"
    MATERIAL_SILVER = "Argent"
    MATERIAL_RAW = "Matières premières"

    # Cryptos
    CRYPTO_L1 = "L1"
    CRYPTO_STABLECOINS = "Stablecoins"
    CRYPTO_DEFI = "DeFi"

    # Exotics
    EXOTIC_GFI = "Forêts"
    EXOTIC_ART = "Art"
    EXOTIC_WATCH = "Watches"

    # Diversified
    UNKNOWN_OPCVM = "OPCVM"

    # Passives
    PASSIVE_VEHICLE = "Véhicule"

    # Unknown (default)
    UNKNOWN = "Unknown"


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
