"""
```{tip}
% TODO
These enumerations are not yet used in Finalynx, but will serve as the basis for the `Analyzer`
subpackage to classify lines and show relevant statistics.
```
"""
from enum import Enum


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
