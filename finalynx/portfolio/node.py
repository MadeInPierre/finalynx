from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import TYPE_CHECKING

import numpy as np
from rich.tree import Tree

from ..config import DEFAULT_CURRENCY
from .constants import LinePerf
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
        currency: Optional[str] = None,
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
        self.currency = currency if currency else DEFAULT_CURRENCY

        if target is not None:
            target.set_parent(self)

        # Setup custom aliases for node rendering
        render_aliases: Dict[str, str] = {
            "[text]": "[target_text][prehint] [name] [hint][newline]",
            "[console]": "[target] [account_code][name_color][name][/] [dim white][hint][/][newline]",
            "[console_ideal]": "[bold green][ideal][/][account_code][name_color][name][/][newline]",
            "[console_deltas]": "[delta][account_code][name_color][name][/][newline]",
            "[console_perf]": "[bold green][perf][/][account_code][name_color][name][/][newline]",
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
            "ideal": self._render_ideal,
            "delta": self._render_delta,
            "perf": self._render_perf,
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

    def get_ideal(self) -> float:
        """:returns: The ideal amount to be invested in this node based on surrounding targets."""
        return self.target.get_ideal()

    def get_delta(self) -> float:
        """:returns: How much should be invested in this node to reach the ideal amount set by the target."""
        return self.get_ideal() - self.get_amount()

    def get_perf(self) -> LinePerf:
        """:returns: The expected yearly performance of this node."""
        raise NotImplementedError("Must be overridden by children classes")

    def get_currency(self) -> str:
        """:returns: This node's currency symbol."""
        return self.currency

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

    def tree_delta(self, _tree: Optional[Tree] = None) -> Tree:
        """Generates a tree with delta amounts to be invested to reach the ideal portfolio allocation."""
        render = self._render_delta(align=False) + ("\n" if self.newline else "")
        return _tree.add(render) if _tree else Tree(render, hide_root=True)

    def process(self) -> None:
        """Some `Node` or `Target` objects might need to process some data once the investment
        values have been fetched from Finary. Here, this method is left as esmpty but can be
        overridden by subclasses.
        """
        return  # Optional method for subclasses to process after fetch

    def _render_currency(self) -> str:
        """:returns: A formatted rendering of this element's currency."""
        return self.get_currency()

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
        """:returns: A formatted rendering of the target goal. This could either be an ideal
        amount or ratio to be reached."""
        return self.target.render_goal()

    def _render_ideal(self) -> str:
        """:returns: A formatted rendering of the ideal amount to be invested based on the target."""
        return self.target.render_ideal()

    def _render_delta(self, align: bool = True, children: Optional[List["Node"]] = None) -> str:
        """Creates a formatted rendering of the delta investment needed to reach the target.
        :param align: Use the `children` parameter as a list of nodes to align all amounts vertically.
        :param children: List of `Node` objects used for vertical alignemnt, defaults to this parent's children.
        :returns: The rendered string.
        """
        delta, check = round(self.get_delta()), self.target.check()
        if delta == 0 or check == Target.RESULT_NONE:
            return ""
        color = "green" if delta > 0 else "red"
        children = children if children else (self.parent.children if self.parent and self.parent.children else [])
        max_length = np.max([len(str(abs(round(c.get_delta())))) for c in children]) if children else 0
        max_length = max_length if align else 0
        if check == Target.RESULT_OK:
            return f"[green]{'✓':>{max_length+3}}[/] "
        return f"[{color}]{'+' if delta > 0 else '-'}{abs(delta):>{max_length}} {self._render_currency()}[/] "

    def _render_perf(self) -> str:
        """:returns: A formatted rendering of the node's expected yearly performance."""
        perf = self.get_perf()
        return f"[{'strike ' if perf.skip else ''}bold green]{perf.expected:.1f} %[/] " if perf else ""

    def _render_name(self) -> str:
        """:returns: A formatted rendering of the node name."""
        return self.name

    def _render_name_color(self) -> str:
        """:returns: A formatted rendering of the node name's color."""
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

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("Must be overridden by subclasses.")
