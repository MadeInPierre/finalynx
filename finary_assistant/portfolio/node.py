import numpy as np
from rich.tree import Tree
from .targets import Target
from .hierarchy import Hierarchy


class Node(Hierarchy):
    def __init__(self, name, parent=None, target=None, newline=False):
        super().__init__(parent)
        self.name = name
        self.newline = newline
        self.target = target if target is not None else Target()
        self.target.set_parent(self)

        if target is not None:
            target.set_parent(self)

    def get_amount(self):
        raise NotImplementedError("Must be implemented by children classes")

    def rich_tree(self, hide_amount=False, _tree=None, **args):
        if _tree is None:
            return Tree(self._render(hide_amount=hide_amount), **args)
        return _tree.add(self._render(hide_amount=hide_amount))

    def process(self):
        return  # Optional method for subclasses to process after fetch

    def _render(self, hide_amount=False):
        hint = (
            f"[dim white] {self.target.hint()}[/]"
            if self.target.check() not in [Target.RESULT_NONE, Target.RESULT_START]
            else ""
        )
        return (
            f"{self._render_amount(hide_amount)} {self._render_name()}"
            + hint
            + self._render_newline()
        )

    def _render_amount(self, hide_amount=False):
        max_length = (
            np.max([len(str(round(c.get_amount()))) for c in self.parent.children])
            if (self.parent and self.parent.children)
            else 0
        )
        return self.target.render_amount(
            n_characters=max_length, hide_amount=hide_amount
        )

    def _render_name(self):
        return self.name

    def _render_newline(self):
        return "\n" if self.newline else ""

    def __repr__(self):
        return f"{self.get_amount()} {self.name}"

    def __str__(self):
        return self._render()
