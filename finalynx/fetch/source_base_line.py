from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from rich.tree import Tree
from unidecode import unidecode

from ..config import get_active_theme as TH
from ..portfolio import Line
from ..portfolio import Portfolio
from .fetch_line import FetchLine
from .source_base import SourceBase


class SourceBaseLine(SourceBase):
    def __init__(self, name: str, cache_validity: int = 12):
        super().__init__(name, FetchLine, "lines", cache_validity)

    def fetch(
        self,
        portfolio: Portfolio,
        clear_cache: bool,
        ignore_orphans: bool,
    ) -> Tree:
        """Fetch data online from a source that contains investment `Line` objects.
        :param clear_cache: Delete cached data to immediately fetch data online, defaults to False
        :param ignore_orphans: If a line in your account is not referenced in your `Portfolio` instance
        then don't attach it to the root (used as a reminder), defaults to False
        :returns: A `Tree` object from the `rich` package used to display what has been fetched.
        """
        tree = self._fetch(clear_cache)

        # If the cache is not empty, Match all lines to the portfolio hierarchy
        for fline in self._fetched_items:
            name = fline.name if fline.name else "Unknown"
            matched_lines: List[Line] = list(set(portfolio.match_lines(fline)))  # merge identical instances

            # Set attributes to the first matched line
            if matched_lines:
                # Issue a warning if multiple lines matched, try to set a stricter key
                if len(matched_lines) > 1:
                    self._log(
                        f"[yellow][bold]Warning:[/] Line matched with multiple nodes, updating first only: {name}",
                        highlight=False,
                    )

                # Update the first line's attributes based on whata has been found online
                fline.update_line(matched_lines[0])

            # If no line matched, attach a fake line to root (unless ignored)
            elif not ignore_orphans:
                self._log(
                    f"[yellow][bold]Warning:[/] Line did not match with any node, attaching to root: {name}"
                    " (ignore with --ignore-orphans)",
                    highlight=False,
                )
                portfolio.add_child(Line(name, amount=fline.amount, currency=fline.currency))

        return tree

    def _register_fetchline(
        self,
        tree_node: Tree,
        name: str,
        id: str,
        account: str,
        amount: int,
        currency: str,
        custom: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Internal method used to register a new investment found from the source."""

        # Skip malformed lines (or lines with 0 euros invested)
        if not (name or id or account) or (amount >= -1.0 and amount < 1.0):
            return

        # Discard non-ASCII characters in the fields
        name, id, account, amount = unidecode(name), str(id), unidecode(account), round(float(amount))

        # Add the line to the rendering tree
        tree_node.add(f"{amount} {currency} {name} [{TH().HINT}]{id=}")

        # Form a FetLine instance from the information given and return it
        self._fetched_items.append(
            FetchLine(name=name, id=id, account=account, custom=custom, amount=amount, currency=currency)
        )
