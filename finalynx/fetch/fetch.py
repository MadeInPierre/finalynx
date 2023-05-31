from typing import Dict
from typing import List
from typing import Optional

from rich.tree import Tree

from ..console import console
from ..portfolio.folder import Portfolio
from .source_base import SourceBase


class Fetch:
    """Entry point class that orchestrates fetching from multiple sources."""

    def __init__(
        self,
        portfolio: Portfolio,
        clear_cache: bool = False,
        ignore_orphans: bool = False,
        sources: Optional[List[SourceBase]] = None,
    ) -> None:
        """This class orchestrates the fetching process from multiple sources."""
        self.portfolio = portfolio
        self._sources: Dict[str, SourceBase] = {s.name: s for s in sources} if sources else {}

        # Flags set by user
        self.clear_cache = clear_cache
        self.ignore_orphans = ignore_orphans

    def add_source(self, source: SourceBase) -> None:
        """Register a new source instance which must already be configured."""
        self._sources[source.id] = source

    def fetch_from(self, active_source_names: List[str]) -> Tree:
        """Fetch from all sources specified in `active_sources` and return a `rich`
        tree used to render what has been fetched to the console."""
        tree = Tree("Fetched data", hide_root=True)

        # Fill the portfolio with info from each activated source
        for source_id in active_source_names:
            if source_id not in self._sources.keys():
                console.log(
                    f"[red][bold]Error:[/] Source '{source_id}' not recognized, have you added it first? Skipping."
                )
                continue
            tree.add(self._sources[source_id].fetch(self.portfolio, self.clear_cache, self.ignore_orphans))

        return tree

    def fetch_all(self) -> Tree:
        """Fetch from all sources added and return a `rich` tree used
        to render what has been fetched to the console."""
        return self.fetch_from(list(self._sources.keys()))
