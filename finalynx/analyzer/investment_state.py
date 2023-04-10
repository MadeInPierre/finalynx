from datetime import date
from typing import Any
from typing import Dict

from ..portfolio import EnvelopeState
from ..portfolio import Folder
from ..portfolio import Line
from ..portfolio import Node
from .analyzer import Analyzer


class AnalyzeInvestmentStates(Analyzer):
    """Aims to agglomerate the children's asset classes and return
    the amount represented by each asset class.
    :returns: a dictionary with asset classes as keys and the
    corresponding total amount contained in the children.
    """

    GRAPH_COLORS = {
        "Unknown": "#434348",
        "Closed": "#577590",
        "Locked": "#F94144",
        "Taxed": "#F9C74F",
        "Free": "#7BB151",  # F8961E
    }

    def analyze(self, target_date: date) -> Dict[str, float]:
        """:returns: A dictionary with keys as the asset class names and values as the
        sum of investments corresponding to each class."""
        return self._recursive_merge(self.node, target_date)

    def _recursive_merge(self, node: Node, target_date: date) -> Dict[str, float]:
        """Internal method for recursive searching."""
        total = {c.value: 0.0 for c in EnvelopeState}

        # Lines simply return their own amount
        if isinstance(node, Line):
            if node.envelope:
                total[node.envelope.get_state(target_date).value] = node.get_amount()
            else:
                total[EnvelopeState.UNKNOWN.value] = node.get_amount()
            return total

        # Folders merge what the children return
        elif isinstance(node, Folder):
            for child in node.children:
                for key, value in self._recursive_merge(child, target_date).items():
                    total[key] += value
            return total

        # Safeguard for future versions
        else:
            raise ValueError(f"Unknown node type '{type(node)}'.")

    def chart(self, target_date: date) -> Dict[str, Any]:
        """:returns: A Highcharts configuration with the data to be displayed."""
        analysis = self.analyze(target_date)

        return {
            "chart": {"plotBackgroundColor": None, "plotBorderWidth": None, "plotShadow": False, "type": "pie"},
            "title": {"text": "Investment States", "align": "center"},
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
                        {"name": key, "y": value, "color": self.GRAPH_COLORS[key]}
                        for i, (key, value) in enumerate(analysis.items())
                    ],
                }
            ],
            "credits": {"enabled": False},
        }
