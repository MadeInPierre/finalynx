from typing import Any
from typing import Dict

from ..portfolio import AssetClass
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

    ASSET_COLORS = {
        "CCP": "#ea5545",
        "Livrets": "#f46a9b",
        "Fonds euro": "#ef9b20",
        "ETFs": "#edbf33",
        "Actions": "#ede15b",
        "Obligations": "#87bc45",
        "Or": "#b33dc6",
        "Cryptos": "#bdcf32",
        "SCPI": "#27aeef",
        "Immobilier": "#00FF00",
        "Passifs": "#434348",
        "Inconnu": "#FF0000",
    }

    def analyze(self) -> Dict[str, float]:
        """:returns: A dictionary with keys as the asset class names and values as the
        sum of investments corresponding to each class."""
        return self._recursive_merge(self.node)

    def _recursive_merge(self, node: Node) -> Dict[str, float]:
        """Internal method for recursive searching."""
        total = {c.value: 0.0 for c in AssetClass}

        # Lines simply return their own amount
        if isinstance(node, Line):
            total[node.asset_class.value] = node.get_amount()
            return total

        # Folders merge what the children return
        elif isinstance(node, Folder):
            for child in node.children:
                for key, value in self._recursive_merge(child).items():
                    total[key] += value
            return total

        # Safeguard for future versions
        else:
            raise ValueError(f"Unknown node type '{type(node)}'.")

    def chart(self) -> Dict[str, Any]:
        """:returns: A Highcharts configuration with the data to be displayed."""
        analysis = self.analyze()

        return {
            "chart": {"plotBackgroundColor": None, "plotBorderWidth": None, "plotShadow": False, "type": "pie"},
            "title": {"text": "Asset classes", "align": "center"},
            "plotOptions": {
                "pie": {
                    "allowPointSelect": True,
                    "cursor": "pointer",
                }
            },
            "series": [
                {
                    "name": "Amount",
                    "colorByPoint": False,
                    "data": [
                        {"name": key, "y": value, "color": self.ASSET_COLORS[key]}
                        for i, (key, value) in enumerate(analysis.items())
                    ],
                }
            ],
            "credits": {"enabled": False},
        }
