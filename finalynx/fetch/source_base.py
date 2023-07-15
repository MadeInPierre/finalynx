import datetime
import json
import os
from typing import Any
from typing import List

from rich.tree import Tree

from ..console import console


class SourceBase:
    """Abstract class to fetch data from multiple sources."""

    def __init__(self, name: str, _type: type, item_name: str, cache_validity: int = 12):
        """This is an abstract class to provide a common interface when fetching investments from
        multiple sources.

        ```{tip}
        Contributions to add data from any format or source are warmly welcome!
        ```

        :param name: A unique name to identify this source instance, the id used to
        activate this source is the lower-case name.
        :param _type: Used by children classes to specify what type of object the source generates.
        :param cache_validity: Finalynx will save fetched results to a file and reuse them on
        the next run if the cache age is less than the specified number of hours.
        """
        self.name = name
        self.cache_validity = cache_validity
        self.cache_fullpath = os.path.join(os.path.dirname(__file__), f"{self.id}_cache.json")
        self._type = _type
        self._item_name = item_name

        # This list will hold all fetched objects
        self._fetched_items: List[Any] = []

    def _fetch(
        self,
        clear_cache: bool,
    ) -> Tree:
        """Fetch items from the source.
        :param clear_cache: Delete cached data to immediately fetch data online, defaults to False
        :returns: A `Tree` object from the `rich` package used to display what has been fetched.
        """
        console.log(f"Fetching data from {self.name}...")

        # Remove the cached data for this source if asked by the user
        if clear_cache and os.path.exists(self.cache_fullpath):
            self._log("Deleting cache per user request.")
            os.remove(self.cache_fullpath)

        # This will hold a key:amount dictionary of all lines found in the source
        self._fetched_items = self._get_cache()  # try to get the data in the cache first
        tree = Tree(self.name, highlight=True, hide_root=True)

        # If there's no valid cache, signin and fetch the data online
        if not self._fetched_items:
            try:
                # Go fetch the data online and populate self._fetched_lines through `_register_fetchline`
                self._fetch_data(tree)
            except Exception as e:
                self._log("[red bold]Error: Couldn't fetch data, please try using the `-f` option to signin again.")
                self._log(f"[red][bold]Details:[/] {e}")
                return tree

            # Save what has been found in a cache file for offline use and better performance at next launch
            self._save_cache()

        # Return a rich tree to be displayed in the console as a recap of what has been fetched
        return tree

    def _fetch_data(self, tree: Tree) -> None:
        """Abstract method, must be averridden by children classes. This method retrieves the data
        from the source, and calls `_register_fetchline` to create a `FetchLine` instance representing
        each fetched investment."""
        raise NotImplementedError("This abstract method must be overriden by all subclasses")

    def _get_cache(self) -> List[Any]:
        """Attempt to retrieve the cached data. Check if more than an hour has passed since the last update.
        :returns: A key:amount dictionary if the cache file is less than an hour old, None otherwise.
        """

        # Abort retrieving cache if the file doesn't exist
        if not os.path.exists(self.cache_fullpath):
            self._log("No cache file found, fetching data.")
            return []

        # Parse the JSON content
        with open(self.cache_fullpath) as f:
            data = json.load(f)

        # Return the cached content if the cache file is less than the maximum age
        last_updated = datetime.datetime.strptime(data["last_updated"], "%Y-%m-%d %H:%M:%S")
        time_diff = datetime.datetime.now() - last_updated
        hours_passed = int(time_diff.total_seconds() // 3600)

        if hours_passed < self.cache_validity:
            self._log(f"Using recently cached data (<{self.cache_validity}h max)")

            # Assume the children class' generated object has a `from_dict` method
            return [self._type.from_dict(line_dict) for line_dict in data[self._item_name]]  # type: ignore
        self._log(f"Fetching data (cache file is {hours_passed}h old > {self.cache_validity}h max)")
        return []

    def _save_cache(self) -> None:
        """Save the fetched data locally to work offline and reduce the amoutn of calls to the API.
        :param tree: Generated tree object containing all information
        """

        # Save current date and time to a JSON file with the fetched data
        self._log(f"Saved fetched data to '{self.cache_fullpath}'")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {"last_updated": current_time, self._item_name: [line.to_dict() for line in self._fetched_items]}
        with open(self.cache_fullpath, "w") as f:
            json.dump(data, f, indent=4)

    def _log(self, message: str, **kwargs: Any) -> None:
        console.log(" " * 4 + message, **kwargs)

    @property
    def id(self) -> str:
        return self.name.lower()
