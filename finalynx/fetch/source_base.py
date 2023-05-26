import datetime
import json
import os
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from rich.tree import Tree
from unidecode import unidecode

from ..console import console
from ..portfolio import Line
from ..portfolio import Portfolio
from .fetch_line import FetchLine


class SourceBase:
    """Abstract class to fetch data from multiple sources."""

    # Finalynx will use the cached data if it is younger than the specified time
    MAX_CACHE_HOURS = 12

    def __init__(
        self,
        name: str,
        clear_cache: bool = False,
        ignore_orphans: bool = False,
    ):
        """This is an abstract class to provide a common interface when fetching investments from
        multiple sources.

        ```{tip}
        Contributions to add data from any format or source are warmly welcome!
        ```

        :param portfolio: A fully configured `Porfolio` instance with your custom investment tree.
        :param cache_filename: Used by subclasses to create separate cache files.
        """
        self.name = name
        self.cache_fullpath = os.path.join(os.path.dirname(__file__), f"{self.id}_cache.json")

        # Flags set by user
        self.clear_cache = clear_cache
        self.ignore_orphans = ignore_orphans

        # This list will hold all fetched line objects.
        self._fetched_lines: List[FetchLine] = []

    def fetch(self, portfolio: Portfolio) -> Tree:
        """Abstract method, requires to be overridden by subclasses.
        :returns: A `Tree` object from the `rich` package used to display what has been fetched.
        """
        with console.status(f"[bold green]Starting fetching from {self.name}..."):
            # Remove the cached data for this source if asked by the user
            if self.clear_cache and os.path.exists(self.cache_fullpath):
                console.log("Deleting cache per user request.")
                os.remove(self.cache_fullpath)

            # This will hold a key:amount dictionary of all lines found in the source
            self._fetched_lines = self._get_cache()  # try to get the data in the cache first
            tree = Tree(self.name, highlight=True, hide_root=True)

            # If there's no valid cache, signin and fetch the data online
            if not self._fetched_lines:
                try:
                    # Go fetch the data online and populate self._fetched_lines through `_register_fetchline`
                    self._fetch_data(tree)
                except Exception as e:
                    console.log(
                        "[red bold]Error: Couldn't fetch data, please try using the `-f` option to signin again."
                    )
                    console.log(f"[red][bold]Details:[/] {e}")
                    return tree

                # Save what has been found in a cache file for offline use and better performance at next launch
                self._save_cache()

            # If the cache is not empty, Match all lines to the portfolio hierarchy
            for fline in self._fetched_lines:
                name = fline.name if fline.name else "Unknown"
                matched_lines: List[Line] = list(set(portfolio.match_lines(fline)))  # merge identical instances

                # Set attributes to the first matched line
                if matched_lines:
                    # Issue a warning if multiple lines matched, try to set a stricter key
                    if len(matched_lines) > 1:
                        console.log(
                            f"[yellow][bold]Warning:[/] Line '{name}' matched with multiple nodes, updating first only."
                        )

                    # Update the first line's attributes based on whata has been found online
                    fline.update_line(matched_lines[0])

                # If no line matched, attach a fake line to root (unless ignored)
                elif not self.ignore_orphans:
                    console.log(
                        f"[yellow][bold]Warning:[/] Line '{name}' did not match with any portfolio node, attaching to root."
                    )
                    portfolio.add_child(Line(name, amount=fline.amount))

            # Return a rich tree to be displayed in the console as a recap of what has been fetched
            console.log(f"Done fetching data from {self.name}.")
        return tree

    def _fetch_data(self, tree: Tree) -> None:
        """Abstract method, must be averridden by children classes. This method retrieves the data
        from the source, and calls `_register_fetchline` to create a `FetchLine` instance representing
        each fetched investment."""
        raise NotImplementedError("This abstract method must be overriden by all subclasses")

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
        """Internal method used to register a new investment found from Finary."""

        # Skip malformed lines (or lines with 0 euros invested)
        if not (name or id or account) or (amount >= -1.0 and amount < 1.0):
            return

        # Discard non-ASCII characters in the fields
        name, id, account, amount = unidecode(name), str(id), unidecode(account), round(float(amount))

        # Add the line to the rendering tree
        tree_node.add(f"{amount} {currency} {name} [dim white]{id=}")

        # Form a FetLine instance from the information given and return it
        self._fetched_lines.append(
            FetchLine(name=name, id=id, account=account, custom=custom, amount=amount, currency=currency)
        )

    def _get_cache(self) -> List[FetchLine]:
        """Attempt to retrieve the cached data. Check if more than an hour has passed since the last update.
        :returns: A key:amount dictionary if the cache file is less than an hour old, None otherwise.
        """

        # Abort retrieving cache if the file doesn't exist
        if not os.path.exists(self.cache_fullpath):
            console.log("No cache file found, fetching data.")
            return []

        # Parse the JSON content
        with open(self.cache_fullpath) as f:
            data = json.load(f)

        # Return the cached content if the cache file is less than the maximum age
        last_updated = datetime.datetime.strptime(data["last_updated"], "%Y-%m-%d %H:%M:%S")
        time_diff = datetime.datetime.now() - last_updated
        hours_passed = int(time_diff.total_seconds() // 3600)

        if hours_passed < self.MAX_CACHE_HOURS:
            console.log(f"Using recently cached data (<{self.MAX_CACHE_HOURS}h max)")
            return [FetchLine.from_dict(line_dict) for line_dict in data["lines"]]
        console.log(f"Fetching data (cache file is {hours_passed}h old > {self.MAX_CACHE_HOURS}h max)")
        return []

    def _save_cache(self) -> None:
        """Save the fetched data locally to work offline and reduce the amoutn of calls to the API.
        :param tree: Generated tree object containing all information
        """

        # Save current date and time to a JSON file with the fetched data
        console.log(f"Saved fetched data to '{self.cache_fullpath}'")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {"last_updated": current_time, "lines": [line.to_dict() for line in self._fetched_lines]}
        with open(self.cache_fullpath, "w") as f:
            json.dump(data, f, indent=4)

    @property
    def id(self) -> str:
        return self.name.lower()
