import numpy as np
from rich.tree import Tree
from .node import Node
from .line import Line
from enum import Enum


class FolderDisplay(Enum):
    EXPANDED = 0
    COLLAPSED = 1
    LINE = 2


class Folder(Node):
    def __init__(
        self,
        name,
        parent=None,
        target=None,
        children=None,
        newline=False,
        display=FolderDisplay.EXPANDED,
    ):
        super().__init__(name, parent, target, newline=False)
        self.children = [] if children is None else children
        self.display = display

        for child in self.children:
            child.set_parent(self)

        if self.children:
            child.newline = newline

    def add_child(self, child):
        child.set_parent(self)
        self.children.append(child)

    def get_amount(self):
        return (
            np.sum([child.get_amount() for child in self.children])
            if self.children
            else 0
        )

    def rich_tree(self, hide_amount=False, _tree=None, **args):
        node = (
            Tree(self._render(hide_amount=hide_amount), guide_style="grey42", **args)
            if _tree is None
            else _tree.add(self._render(hide_amount=hide_amount))
        )
        if self.display == FolderDisplay.EXPANDED:
            for child in self.children:
                child.rich_tree(hide_amount=hide_amount, _tree=node)
        return node

    def process(self):
        for child in self.children:
            child.process()

    def set_child_amount(self, key, amount):
        success = False
        for child in self.children:
            if isinstance(child, Line) and child.key == key:
                child.amount = amount
                success = True
            elif (
                isinstance(child, Folder)
                and child.set_child_amount(key, amount) == True
            ):
                success = True
        return success

    def _render_name(self):
        if self.display == FolderDisplay.LINE:
            return self.name
        return f"[blue bold]{self.name}[/]"

    def _render_newline(self):
        return ""
