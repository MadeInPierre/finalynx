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


@dataclass
class Asset:
    """Asset subclass definition class."""

    name: str
    asset_class: AssetClass


class Assets(Enum):
    """Default collection of assets used as asset subclasses (for easier visualization and analysis)."""

    # Cash
    CASH_CCP = Asset("Comptes courants", AssetClass.CASH)
    CASH_MONETARY = Asset("Monétaire", AssetClass.CASH)

    # Guaranteed investments (mostly french)
    GUARANTEED_LIVRET = Asset("Livrets", AssetClass.GUARANTEED)
    GUARANTEED_LIVRET_TAXED = Asset("Livrets imposables", AssetClass.GUARANTEED)
    GUARANTEED_FOND_EURO = Asset("Fonds euro", AssetClass.GUARANTEED)

    # Bonds
    BOND_DATED = Asset("Fonds datés", AssetClass.BOND)
    BOND_ETF = Asset("ETFs Obligations", AssetClass.BOND)

    # Stocks
    STOCK_SHARE = Asset("Titres vifs", AssetClass.STOCK)
    STOCK_ETF = Asset("ETFs Actions", AssetClass.STOCK)

    # Real estate
    REAL_ESTATE_PHYSICAL = Asset("Immobilier physique", AssetClass.REAL_ESTATE)
    REAL_ESTATE_SCPI = Asset("SCPI", AssetClass.REAL_ESTATE)
    REAL_ESTATE_SCI = Asset("SCI", AssetClass.REAL_ESTATE)

    # Metals
    MATERIAL_GOLD = Asset("Or", AssetClass.MATERIAL)
    MATERIAL_SILVER = Asset("Argent", AssetClass.MATERIAL)
    MATERIAL_RAW = Asset("Matières premières", AssetClass.MATERIAL)

    # Cryptos
    CRYPTO_L1 = Asset("L1", AssetClass.CRYPTO)
    CRYPTO_STABLECOINS = Asset("Stablecoins", AssetClass.CRYPTO)
    CRYPTO_DEFI = Asset("DeFi", AssetClass.CRYPTO)

    # Exotics
    EXOTIC_GFI = Asset("Forêts", AssetClass.EXOTIC)
    EXOTIC_ART = Asset("Art", AssetClass.EXOTIC)
    EXOTIC_WATCH = Asset("Watches", AssetClass.EXOTIC)

    # Diversified
    UNKNOWN_OPCVM = Asset("OPCVM", AssetClass.DIVERSIFIED)

    # Passives
    PASSIVE_VEHICLE = Asset("Véhicule", AssetClass.PASSIVE)


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
