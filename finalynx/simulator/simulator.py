from typing import List
from typing import Optional

from ..portfolio.portfolio import Portfolio


class Simulator:
    def __init__(self, events: Optional[List[str]] = None):
        self.events = [] if events is None else events

    def rich_simulation(self, portfolio: Portfolio) -> str:
        return "Simulation"
