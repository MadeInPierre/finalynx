from rich.tree import Tree

from .source_base import SourceBase


class MySource(SourceBase):
    # No spaces, alphanumeric name only
    SOURCE_NAME = "MySourceName"

    def __init__(self, clear_cache: bool = False, ignore_orphans: bool = False) -> None:
        """Write a description of how your source works here, with a list of what each
        argument does:
        :param clear_cache: Forces to clear the last fetch's saved results.
        :param ignore_orphans: Don't create new lines at the root of the portfolio if some
        investments have been fetched but have not been matched with any existing node.
        """
        super().__init__(self.SOURCE_NAME, clear_cache, ignore_orphans)

    def _fetch_data(self, tree: Tree) -> None:
        """Use this method to fetch your data however you want! CSV, PDF, API, manual input...
        Use any logic you want here! Just use this method once you have fetched an investment:
        """

        # Display the lines found to the console, you can create a nested tree if you want
        node = tree.add("This a category example")

        # Register the real investment information, will be cached and matched to the portfolio
        self._register_fetchline(
            tree_node=node,  # this line will display under the category, use `tree` for root
            name="My Investment",
            id="123",
            account="My Account",
            amount=10000,
            currency="€",
        )
