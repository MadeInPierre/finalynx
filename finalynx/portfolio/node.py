from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import TYPE_CHECKING

import numpy as np
from rich.tree import Tree

from .hierarchy import Hierarchy
from .render import Render
from .targets import Target

if TYPE_CHECKING:
    from .folder import Folder


class Node(Hierarchy, Render):
    """Abstract class that represents an element in the Portfolio tree."""

    def __init__(
        self,
        name: str,
        parent: Optional["Folder"] = None,
        target: Optional[Target] = None,
        newline: bool = False,
        aliases: Optional[Dict[str, str]] = None,
        agents: Optional[Dict[str, Callable[..., str]]] = None,
    ):
        """This is an abstract class used by the `Line` and `Folder` subclasses.

        :param name: The name that will be displayed in the final portfolio tree.
        :param parent: Parent of this node, passed up to the superclass `Hierarchy`.
        :param target: Optional `Target` instance to format this line's amount based on the objective you selected.
        :param newline: Print a new line in the console at the end of this `Line` for better readability.
        :param aliases: Add or replace render aliases used when specifying a render format.
        :param agents: Add or replace keywords associated to rendering callbacks.
        """
        Hierarchy.__init__(self, parent)

        self.parent: Optional["Folder"] = parent
        self.name: str = name
        self.newline = newline
        self.target = target if target is not None else Target()
        self.target.set_parent(self)

        if target is not None:
            target.set_parent(self)

        # Setup custom aliases for node rendering
        render_aliases: Dict[str, str] = {
            "[text]": "[target_text][prehint] [name] [hint][newline]",
            "[console]": "[target][dim white][prehint][/] [account_code][name_color][name][/] [dim white][hint][/][newline]",
            "[console_targets]": "[bold green][goal][/][account_code][name_color][name][/][newline]",
            "[text_targets]": "[goal][name][newline]",
            "[dashboard_tree]": "[amount] [currency] [name]",
            "[dashboard_console]": "[bold][target][/][bright_black][prehint][/] [name_color][name][/] [bright_black][hint][/][newline]",
            "[target]": "[[target_color]][target_text][/]",
            "[target_text]": "[target_symbol] [amount] [currency]",
        }
        render_agents: Dict[str, Callable[..., str]] = {
            "name": self._render_name,
            "name_color": self._render_name_color,
            "newline": self._render_newline,
            "amount": self._render_amount,
            "goal": self._render_goal,
            "hint": self._render_hint,
            "prehint": self._render_prehint,
            "currency": self._render_currency,
            "target_symbol": self.target._render_target_symbol,
            "target_color": self.target._render_target_color,
        }
        render_aliases.update(aliases if aliases else {})
        render_agents.update(agents if agents else {})
        Render.__init__(self, render_aliases, render_agents)

    def get_amount(self) -> float:
        """Virtual method that must be implemented by all subclasses."""
        raise NotImplementedError("Must be implemented by children classes")

    def tree(
        self,
        output_format: str = "[console]",
        _tree: Optional[Tree] = None,
        hide_root: bool = False,
        **render_args: Any,
    ) -> Tree:
        """Generate a fully rendered `Tree` object from the `rich` package using the specified format.

        This `Tree` can either be manipulated for further operations or directly printed
        to the console using rich's `print` method.

        :param hide_amount: Replace the amounts by simple dots (easier to share the result), defaults to False.
        :param _tree: Internal method to pass the folder's root tree object to the children.
        :param args: Provide any list of arguments supported by the `Tree` class if this is the root folder in the hierarchy.
        :returns: If the `_tree` argument is empty, the function returns a new `Tree` instance with this node's render.
        Otherwise, it adds this node's render as a child node and returns the `_tree`.
        """
        render = self.render(output_format, **render_args)
        return _tree.add(render) if _tree else Tree(render, hide_root=hide_root)

    def process(self) -> None:
        """Some `Node` or `Target` objects might need to process some data once the investment
        values have been fetched from Finary. Here, this method is left as esmpty but can be
        overridden by subclasses.
        """
        return  # Optional method for subclasses to process after fetch

    def _render_currency(self) -> str:
        """:returns: A formatted rendering of this element's currency."""
        return "€"  # TODO add multi-currency support?

    def _render_hint(self) -> str:
        """:returns: A formatted rendering of a hint message (at the end by default)."""
        return self.target.hint() if self.target.check() != Target.RESULT_NONE else ""

    def _render_prehint(self) -> str:
        """:returns: A formatted rendering of a pre-hint message (next to the amount by default)."""
        prehint = self.target.prehint()
        return " " + prehint if prehint else ""

    def _render_amount(self, hide_amounts: bool = False) -> str:
        """:returns: A formatted rendering of the node amount aligned with the other
        elements in the same parent.
        :param hide_amounts: Replaces amoutn with a dummy amount with dots instead of
        the real amount (easier to share).
        """
        max_length = (
            np.max([len(str(round(c.get_amount()))) for c in self.parent.children])
            if (self.parent and self.parent.children)
            else 0
        )
        return "···" if hide_amounts else f"{round(self.get_amount()):>{max_length}}"

    def _render_goal(self) -> str:
        return self.target.render_goal()

    def _render_name(self) -> str:
        """:returns: A formatted rendering of the node name."""
        return self.name

    def _render_name_color(self) -> str:
        """:returns: A formatted rendering of the node name."""
        return "[black]"

    def _render_newline(self) -> str:
        """:returns: A rendering of the newline if set by the user."""
        return "\n" if self.newline else ""

    def __repr__(self) -> str:
        """:returns: A console representation of this node for debugging."""
        return self.render("[amount] [name]")

    def __str__(self) -> str:
        """:returns: The formatted console rendering of this node."""
        return self.render()
