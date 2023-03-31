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

    def analyze(self) -> Dict[str, float]:
        """:returns: A dictionary with keys as the asset class names and values as the
        sum of investments corresponding to each class."""
        return self._recursive_merge(self.node)

    def _recursive_merge(self, node: Node) -> Dict[str, float]:
        """Internal method for recursive searching."""

        # Lines simply return their own amount
        if isinstance(node, Line):
            return {node.asset_class.value: node.get_amount()}

        # Folders merge what the children return
        elif isinstance(node, Folder):
            total = {c.value: 0.0 for c in AssetClass}
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
                    "name": "Brands",
                    "colorByPoint": True,
                    "data": [{"name": key, "y": value} for key, value in analysis.items() if value > 0],
                }
            ],
            "credits": {"enabled": False},
        }
