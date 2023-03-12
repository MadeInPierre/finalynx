"""
```{tip}
TODO Dummy class for now, check back later or help us by contributing!
```
"""
from typing import List
from typing import Optional

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
