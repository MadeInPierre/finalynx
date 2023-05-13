from typing import Any
from typing import Dict

import numpy as np

from ..portfolio import AssetClass
from ..portfolio import AssetSubclass
from ..portfolio import Folder
from ..portfolio import Line
from ..portfolio import Node
from .analyzer import Analyzer


class AnalyzeAssetClasses(Analyzer):
    """Aims to agglomerate the children's asset classes and return
    the amount represented by each asset class.
    :returns: a dictionary with asset classes as keys and the
    corresponding total amount contained in the children.
    """

    ASSET_COLORS_FINARY = {
        # "Cash": "#eed7b4",
        # "Livrets": "#b966f5",
        # "Fonds euro": "#228c83",
        # "Actions": "#3a84de",
        # "Obligations": "#87bc45",
        # "Or": "#77cfac",
        # "Cryptos": "#bdcf32",
        # "Immobilier": "#deab5e",
        # "Passifs": "#434348",
        # "Inconnu": "#b54053",
        "Cash": "#eed7b4",
        "Garanti": "#b966f5",
        "Obligations": "#87bc45",
        "Actions": "#3a84de",
        "Immobilier": "#deab5e",
        "Métaux": "#77cfac",
        "Cryptos": "#bdcf32",
        "Passifs": "#434348",
        "Exotiques": "#228c83",
        "Inconnu": "#b54053",
        "Diversifié": "#b54093",
    }

    ASSET_COLORS_CUSTOM = {
        # "Cash": "#7BB151",
        # "Livrets": "#43AA8B",
        # "Fonds euro": "#4D908E",
        # "Obligations": "#577590",
        # "Actions": "#277DA1",
        # "Or": "#F9C74F",
        # "Immobilier": "#deab5e",
        # "Cryptos": "#F94144",
        # "Passifs": "#434348",
        # "Inconnu": "#999999",
        "Cash": "#7BB151",
        "Garanti": "#43AA8B",
        # "Fonds euro": "#4D908E",
        "Obligations": "#577590",
        "Actions": "#277DA1",
        "Métaux": "#F9C74F",
        "Immobilier": "#deab5e",
        "Cryptos": "#F94144",
        "Passifs": "#434348",
        "Exotiques": "#660099",
        "Inconnu": "#999999",
        "Diversifié": "#b54093",
    }

    def analyze(self) -> Dict[str, Any]:
        """:returns: A dictionary with keys as the asset class names and values as the
        sum of investments corresponding to each class."""
        return self._recursive_merge(self.node)

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

    def chart(self, color_map: str = "finary") -> Dict[str, Any]:
        """:returns: A Highcharts configuration with the data to be displayed."""
        analysis = self.analyze()
        total = np.sum([analysis[k]["total"] for k in analysis.keys()])
        colors = self.ASSET_COLORS_FINARY if color_map == "finary" else self.ASSET_COLORS_CUSTOM

        return {
            "chart": {"plotBackgroundColor": None, "plotBorderWidth": None, "plotShadow": False, "type": "pie"},
            "title": {"text": "Asset Classes", "align": "center"},
            "plotOptions": {
                "pie": {
                    "allowPointSelect": True,
                    "cursor": "pointer",
                }
            },
            "tooltip": {"valueSuffix": " €"},
            "series": [
                {
                    "name": "Amount",
                    "colorByPoint": False,
                    "size": "55%",
                    "data": [
                        {
                            "name": class_name if class_dict["total"] / total > 0.03 else "",
                            "y": class_dict["total"],
                            "color": colors[class_name],
                        }
                        for class_name, class_dict in analysis.items()
                        if class_dict["total"] > 0
                    ],
                    "dataLabels": {
                        "distance": -20,
                    },
                },
                {
                    "name": "Amount",
                    "size": "80%",
                    "innerSize": "75%",
                    "data": [
                        {
                            "name": subclass_name,
                            "y": subclass_value,
                            "color": colors[class_name] + "C0",
                        }
                        for class_name, class_dict in analysis.items()
                        for subclass_name, subclass_value in class_dict["subclasses"].items()
                        if subclass_value > 0
                    ],
                },
            ],
            "credits": {"enabled": False},
        }
