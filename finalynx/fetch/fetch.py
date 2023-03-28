import os

from rich.tree import Tree

from ..portfolio import Portfolio


class Fetch:
    """Abstract class to fetch data from multiple sources."""

    MAX_CACHE_HOURS = 12

    def __init__(self, portfolio: Portfolio, cache_filename: str):
        """This is an abstract class to provide a common interface when fetching investments from
        multiple sources.

        ```{tip}
        Contributions to add data from any format or source are warmly welcome!
        ```

        :param portfolio: A fully configured `Porfolio` instance with your custom investment tree.
        :param cache_filename: Used by subclasses to create separate cache files.
        """
        self.cache_fullpath = os.path.join(os.path.dirname(__file__), cache_filename)
        self.portfolio = portfolio

    def fetch(self) -> Tree:
        """Abstract method, requires to be overridden by subclasses.
        :returns: A `Tree` object from the `rich` package used to display what has been fetched.
        """
        raise NotImplementedError("This abstract method must be overriden by all subclasses")
