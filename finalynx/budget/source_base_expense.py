from typing import List

from rich.tree import Tree

from ..console import console
from ..fetch.source_base import SourceBase
from .expense import Expense


class SourceBaseExpense(SourceBase):
    def __init__(self, name: str, cache_validity: int = 12):
        super().__init__(name, Expense, "expenses", cache_validity)
        self._fetched_items: List[Expense]

    def fetch(
        self,
        clear_cache: bool,
    ) -> Tree:
        """Fetch data online from a source that contains investment `Line` objects.
        :param list_expen
        :param clear_cache: Delete cached data to immediately fetch data online, defaults to False
        :returns: A lsit of `Expense` objects fetched from the source.
        """
        return self._fetch(clear_cache)  # No need for the `Tree` in expenses

    def get_expenses(self) -> List[Expense]:
        """:returns: The list of expenses found after calling `fetch()`."""
        assert self._fetched_items, "Call fetch() first"
        return self._fetched_items

    def _register_expense(
        self,
        timestamp: int,
        amount: float,
        currency: str,
        merchant_name: str,
        merchant_category: str,
    ) -> None:
        """Internal method used to register a new expense found from the source."""

        # Skip malformed lines
        if not timestamp or len(currency) != 1:
            console.log("[yellow][bold]Warning:[/] Skipping malformed expense.")
            return

        # Make sure types are correct (you know, Python)
        timestamp, amount = int(timestamp), float(amount)

        # Form an Expense instance from the information given and save it
        self._fetched_items.append(Expense(timestamp, amount, merchant_name, merchant_category))
