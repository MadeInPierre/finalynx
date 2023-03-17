from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

import numpy as np
from rich.tree import Tree

from .hierarchy import Hierarchy
from .targets import Target

if TYPE_CHECKING:
    from .folder import Folder


class Node(Hierarchy):
    """Abstract class that represents an element in the Portfolio tree."""

    def __init__(
        self, name: str, parent: Optional["Folder"] = None, target: Optional[Target] = None, newline: bool = False
    ):
        """This is an abstract class used by the `Line` and `Folder` subclasses.

        :param name: The name that will be displayed in the final portfolio tree.
        :param parent: Parent of this node, passed up to the superclass `Hierarchy`.
        :param target: Optional `Target` instance to format this line's amount based on the objective you selected.
        :param newline: Print a new line in the console at the end of this `Line` for better readability.
        """
        super().__init__(parent)
        self.parent: Optional["Folder"] = parent
        self.name: str = name
        self.newline = newline
        self.target = target if target is not None else Target()
        self.target.set_parent(self)

        if target is not None:
            target.set_parent(self)

    def get_amount(self) -> float:
        """Virtual method that must be implemented by all subclasses."""
        raise NotImplementedError("Must be implemented by children classes")

    def tree(self, format: str = "rich", hide_amount: bool = False, _tree: Optional[Tree] = None, **args: Any) -> Tree:
        """Generate a fully rendered `Tree` object from the `rich` package using the

        This `Tree` can either be manipulated for further operations or directly printed
        to the console using rich's `print` method.

        :param hide_amount: Replace the amounts by simple dots (easier to share the result), defaults to False.
        :param _tree: Internal method to pass the folder's root tree object to the children.
        :param args: Provide any list of arguments supported by the `Tree` class if this is the root folder in the hierarchy.
        :returns: If the `_tree` argument is empty, the function returns a new `Tree` instance with this node's render.
        Otherwise, it adds this node's render as a child node and returns the `_tree`.
        """
        if _tree is None:
            return Tree(self._render(format=format, hide_amount=hide_amount), **args)
        return _tree.add(self._render(format=format, hide_amount=hide_amount))

    def process(self) -> None:
        """Some `Node` or `Target` objects might need to process some data once the investment
        values have been fetched from Finary. Here, this method is left as esmpty but can be
        overridden by subclasses.
        """
        return  # Optional method for subclasses to process after fetch

    def _render(
        self, format: str = "rich", hide_amount: bool = False
    ) -> str:  # TODO rename without underscore? create modular format?
        """Generate a rich-formatted output to the console about this node.
        :param hide_amount: Replace the amounts by simple dots (easier to share the result), defaults to False.
        :returns: A rich-formatted string with every element in the node (e.g. target, name, objective, and so on).
        """
        if format == "rich":
            hint = (
                f"[dim white] {self.target.hint()}[/]"
                if self.target.check() not in [Target.RESULT_NONE, Target.RESULT_START]
                else ""
            )
            return (
                f"{self._render_amount(hide_amount)} {self._render_name()}"
                + hint  # noqa: W503
                + self._render_newline()  # noqa: W503
            )
        elif format == "name":
            return self._render_name()
        else:
            raise ValueError("Render type '{format}' is unrecognized.")

    def _render_amount(self, hide_amount: bool = False) -> str:
        """:returns: A rendering of the amoutn invested in this node. This function aligns the units
        between nodes sharing the same parent."""
        max_length = (
            np.max([len(str(round(c.get_amount()))) for c in self.parent.children])
            if (self.parent and self.parent.children)
            else 0
        )

        return self.target.render_amount(n_characters=max_length, hide_amount=hide_amount)

    def _render_name(self) -> str:
        """:returns: A formatted rendering of this node's name."""
        return self.name

    def _render_newline(self) -> str:
        """:returns: A rendering of the newline if set by the user."""
        return "\n" if self.newline else ""

    def __repr__(self) -> str:
        """:returns: A console representation of this node for debugging."""
        return f"{self.get_amount()} {self.name}"

    def __str__(self) -> str:
        """:returns: The formatted console rendering of this node."""
        return self._render()
