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
    def __init__(
        self, name: str, parent: Optional["Folder"] = None, target: Optional[Target] = None, newline: bool = False
    ):
        super().__init__(parent)
        self.parent: Optional["Folder"] = parent
        self.name: str = name
        self.newline = newline
        self.target = target if target is not None else Target()
        self.target.set_parent(self)

        if target is not None:
            target.set_parent(self)

    def get_amount(self) -> float:
        raise NotImplementedError("Must be implemented by children classes")

    def rich_tree(self, hide_amount: bool = False, _tree: Optional[Tree] = None, **args: Any) -> Tree:
        if _tree is None:
            return Tree(self._render(hide_amount=hide_amount), **args)
        return _tree.add(self._render(hide_amount=hide_amount))

    def process(self) -> None:
        return  # Optional method for subclasses to process after fetch

    def _render(self, hide_amount: bool = False) -> str:
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

    def _render_amount(self, hide_amount: bool = False) -> str:
        max_length = (
            np.max([len(str(round(c.get_amount()))) for c in self.parent.children])
            if (self.parent and self.parent.children)
            else 0
        )

        return self.target.render_amount(n_characters=max_length, hide_amount=hide_amount)

    def _render_name(self) -> str:
        return self.name

    def _render_newline(self) -> str:
        return "\n" if self.newline else ""

    def __repr__(self) -> str:
        return f"{self.get_amount()} {self.name}"

    def __str__(self) -> str:
        return self._render()
