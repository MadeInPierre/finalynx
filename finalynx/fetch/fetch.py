from typing import Dict
from typing import List
from typing import Optional

from rich.tree import Tree

from ..portfolio.folder import Portfolio
from .source_base import SourceBase


class Fetch:
    """Entry point class that orchestrates fetching from multiple sources."""

    def __init__(
        self,
        portfolio: Portfolio,
        sources: Optional[List[SourceBase]] = None,
    ) -> None:
        """This class orchestrates the fetching process from multiple sources."""
        self.portfolio = portfolio
        self._sources: Dict[str, SourceBase] = {s.name: s for s in sources} if sources else {}

    def add_source(self, source: SourceBase) -> None:
        """Register a new source instance which must already be configured."""
        self._sources[source.id] = source

    def fetch_from(self, active_source_names: List[str]) -> Tree:
        """Fetch from all sources specified in `active_sources` and return a `rich`
        tree used to render what has been fetched to the console."""
        tree = Tree("Fetched data")

        # Fill the portfolio with info from each activated source
        for source_id, source in self._sources.items():
            if source_id in active_source_names:
                tree.add(source.fetch(self.portfolio))

        return tree

    def fetch_all(self) -> Tree:
        """Fetch from all sources added and return a `rich` tree used
        to render what has been fetched to the console."""
        return self.fetch_from(list(self._sources.keys()))
