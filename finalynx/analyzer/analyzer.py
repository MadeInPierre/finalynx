"""
```{tip}
TODO Dummy class for now, check back later or help us by contributing!
```
"""
from typing import Any
from typing import Dict

from ..portfolio import Node


class Analyzer:
    """
    Main class for generating modular graphs and statistics about your portfolio.

    This module has not started development yet. Check back soon!
    """

    def __init__(self, node: Node):
        self.node = node

    def analyze(self) -> Any:
        """Abstract method, must be overridden by subclasses to return the analysis result."""
        raise NotImplementedError("Method must be overridden by a subclass.")

    def chart(self) -> Dict[Any, Any]:
        """Abstract method, must be overridden by subclasses to return a Highcharts configuration
        (will be shown in the web dashboard)."""
        raise NotImplementedError("Method must be overridden by a subclass.")
