from typing import Any
from typing import Dict

from ..portfolio import AssetClass
from ..portfolio import AssetSubclass
from ..portfolio import Folder
from ..portfolio import Line
from ..portfolio import Node
from .analyzer import Analyzer


class AnalyzeAssetSubclasses(Analyzer):
    """Aims to agglomerate the children's Sub asset classes and return
    the amount represented by each Sub asset class.
    :returns: a dictionary with Sub asset classes as keys and the
    corresponding total amount contained in the children.
    """

    SUBASSET_COLORS_FINARY = {
        # Cash
        "Comptes courants": "#eed7b4",
        "Monétaire": "#eed7b4",
        "Liquidités": "#eed7b4",
        # Guaranteed investments (mostly french)
        "Livrets": "#b966f5",
        "Livrets imposables": "#b966f5",
        "Fonds euro": "#b966f5",
        # Bonds
        "Fonds datés": "#87bc45",
        # Stocks
        "Titres vifs": "#3a84de",
        "ETF": "#3a84de",
        # Real estate
        "Immobilier physique": "#deab5e",
        "SCPI": "#deab5e",
        "SCI": "#deab5e",
        # Metals
        "Or": "#77cfac",
        "Argent": "#77cfac",
        "Matières premières": "#77cfac",
        # Cryptos
        "L1": "#bdcf32",
        "Stablecoins": "#bdcf32",
        "DeFi": "#bdcf32",
        # Passives
        "Véhicule": "#434348",
        "Passif": "#434348",
        # Exotics
        "Forêts": "#228c83",
        "Art": "#228c83",
        "Watches": "#228c83",
        "Crowdlending": "#228c83",
        "Startup": "#228c83",
        # Diversified
        "Diversifié": "#b54093",
        "OPCVM": "#b54093",
        # Unknown (default)
        "Unknown": "#b54053",
    }

    SUBASSET_COLORS_CUSTOM = {
        # Cash
        "Comptes courants": "#eed7b4",
        "Monétaire": "#eed7b4",
        "Liquidités": "#eed7b4",
        # Guaranteed investments (mostly french)
        "Livrets": "#b966f5",
        "Livrets imposables": "#b966f5",
        "Fonds euro": "#b966f5",
        # Bonds
        "Fonds datés": "#87bc45",
        # Stocks
        "Titres vifs": "#3a84de",
        "ETF": "#3a84de",
        # Real estate
        "Immobilier physique": "#deab5e",
        "SCPI": "#deab5e",
        "SCI": "#deab5e",
        # Metals
        "Or": "#77cfac",
        "Argent": "#77cfac",
        "Matières premières": "#77cfac",
        # Cryptos
        "L1": "#bdcf32",
        "Stablecoins": "#bdcf32",
        "DeFi": "#bdcf32",
        # Passives
        "Véhicule": "#434348",
        "Passif": "#434348",
        # Exotics
        "Forêts": "#228c83",
        "Art": "#228c83",
        "Watches": "#228c83",
        "Crowdlending": "#228c83",
        "Startup": "#228c83",
        # Diversified
        "Diversifié": "#b54093",
        "OPCVM": "#b54093",
        # Unknown (default)
        "Unknown": "#b54053",
    }

    def analyze(self) -> Dict[str, Any]:
        """:returns: A dictionary with keys as the asset class names and values as the sum of
        investments corresponding to each class. Two-layer dictionary with classes and subclasses."""
        return self._recursive_merge(self.node)

    def analyze_flat(self) -> Dict[str, float]:
        """:returns: A dictionary with keys as the Sub asset class names and values as the
        sum of investments corresponding to each subclass."""
        return self._recursive_merge_flat(self.node)

    def _recursive_merge_flat(self, node: Node) -> Dict[str, Any]:
        """Internal method for recursive searching."""
        total = {}

        # Lines simply return their own amount
        if isinstance(node, Line):
            total[node.asset_subclass.value] = node.get_amount()
            return total

        # Folders merge what the children return
        elif isinstance(node, Folder):
            for child in node.children:
                for key, value in self._recursive_merge_flat(child).items():
                    if key in total.keys():
                        total[key] += value
                    else:
                        total[key] = value
                    # for subkey, subvalue in value["subclasses"].items():
                    #     total[subkey] += subvalue
            return total

        # Safeguard for future versions
        else:
            raise ValueError(f"Unknown node type '{type(node)}'.")

    def _recursive_merge(self, node: Node) -> Dict[str, Any]:
        """Internal method for recursive searching."""
        result: Dict[str, Any] = {
            c.value: {"total": 0.0, "subclasses": {s.value: 0.0 for s in AssetSubclass}} for c in AssetClass
        }

        # Lines simply return their own amount
        if isinstance(node, Line):
            result[node.asset_class.value]["total"] = node.get_amount()
            result[node.asset_class.value]["subclasses"][node.asset_subclass.value] = node.get_amount()
            return result

        # Folders merge what the children return
        elif isinstance(node, Folder):
            for child in node.children:
                for key, subdict in self._recursive_merge(child).items():
                    result[key]["total"] += subdict["total"]

                    for subkey, subvalue in subdict["subclasses"].items():
                        result[key]["subclasses"][subkey] += subvalue
            return result

        # Safeguard for future versions
        else:
            raise ValueError(f"Unknown node type '{type(node)}'.")
