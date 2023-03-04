from enum import Enum


class AssetType(Enum):
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
