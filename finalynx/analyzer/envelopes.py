from typing import Any
from typing import Dict

from ..portfolio import Folder
from ..portfolio import Line
from ..portfolio import Node
from .analyzer import Analyzer


class AnalyzeEnvelopes(Analyzer):
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
        total = {}

        # Lines simply return their own amount
        if isinstance(node, Line):
            if node.envelope:
                total[node.envelope.name] = node.get_amount()
            else:
                total["Unknown"] = node.get_amount()
            return total

        # Folders merge what the children return
        elif isinstance(node, Folder):
            for child in node.children:
                for key, value in self._recursive_merge(child).items():
                    if key in total.keys():
                        total[key] += value
                    else:
                        total[key] = value
            return total

        # Safeguard for future versions
        else:
            raise ValueError(f"Unknown node type '{type(node)}'.")

    def chart(self) -> Dict[str, Any]:
        """:returns: A Highcharts configuration with the data to be displayed."""
        analysis = self.analyze()

        return {
            "chart": {"plotBackgroundColor": None, "plotBorderWidth": None, "plotShadow": False, "type": "pie"},
            "title": {"text": "Envelopes", "align": "center"},
            "plotOptions": {
                "pie": {
                    "allowPointSelect": True,
                    "cursor": "pointer",
                }
            },
            "series": [
                {
                    "name": "Amount",
                    "data": [{"name": key, "y": value} for i, (key, value) in enumerate(analysis.items())],
                }
            ],
            "credits": {"enabled": False},
        }
