"""
```{tip}
TODO Dummy class for now, check back later or help us by contributing!
```
"""
from datetime import date
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from finalynx.analyzer.investment_state import AnalyzeInvestmentStates
from finalynx.portfolio.envelope import EnvelopeState

from ..portfolio.portfolio import Portfolio


class Simulator:
    """
    Main class for generating modular graphs about your life events and portfolio evolution.

    This module has not started development yet. Check back soon!
    """

    def __init__(self, events: Optional[List[str]] = None):
        """Empty initialization for now."""
        self.events = [] if events is None else events

    def rich_simulation(self, portfolio: Portfolio) -> str:
        """Dummy output for now, will return a full simulation graph in the future."""
        return "Simulation"

    def chart(self, portfolio: Portfolio) -> Dict[str, Any]:
        analyzer = AnalyzeInvestmentStates(portfolio)
        data: Dict[str, List[float]] = {c.value: [] for c in EnvelopeState}

        for year in range(2000, 2100):
            result = analyzer.analyze(date(year, 1, 1))
            for key, value in result.items():
                data[key].append(value)

        colors = {
            "Unknown": "#434348",
            "Closed": "#999999",
            "Locked": "#F94144",
            "Taxed": "#F9C74F",
            "Free": "#7BB151",
        }

        return {
            "chart": {"plotBackgroundColor": None, "plotBorderWidth": None, "plotShadow": False, "type": "area"},
            "title": {"text": "Simulation", "align": "center"},
            "plotOptions": {
                "series": {"pointStart": 2000},
                "area": {
                    "stacking": "normal",
                    "lineColor": "#666666",
                    "lineWidth": 1,
                    "marker": {"lineWidth": 1, "lineColor": "#666666"},
                },
            },
            "series": [{"name": key, "data": value, "color": colors[key]} for key, value in data.items()],
            "credits": {"enabled": False},
            # "xAxis": {"plotLines": [{"color": "#000000", "width": 2, "value": 2023}]},
        }
