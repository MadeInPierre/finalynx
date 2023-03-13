"""
```{tip}
% TODO
These enumerations are not yet used in Finalynx, but will serve as the basis for the `Analyzer`
subpackage to classify lines and show relevant statistics.
```
"""
from enum import Enum


class AssetType(Enum):
    """Enumeration that defines the asset class for each line."""

    CCP = "CCP"
    LIVRET = "Livret"
    FOND_EURO = "Fonds euro"
    ETF = "ETF"
    STOCK = "Action"
    OBLIGATION = "Obligation"
    CROWDFUNDING = "Crowdfunding"
    GOLD = "Or"
    SILVER = "Argent"
    PILOTED = "Gestion pilotee"
    CRYPTO = "Cryptos"
    FOREST = "Forets"
    SCPI = "SCPI"
    HOUSING = "Immobilier"
    PASSIVE = "Passif"


class EnvelopeType(Enum):
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
