import numpy as np
from rich.tree import Tree
from .node import Node
from .line import Line


class Folder(Node):
    def __init__(self, name, parent=None, target=None, children=None):
        super().__init__(name, parent, target)
        self.children = [] if children is None else children

        for child in self.children:
            child.set_parent(self)
    
    def add_child(self, child):
        child.set_parent(self)
        self.children.append(child)
    
    def get_amount(self):
        return np.sum([child.get_amount() for child in self.children]) if self.children else 0

    def build_tree(self, tree=None, **args):
        node = Tree(str(self), guide_style='blue', **args) if tree is None else tree.add(str(self))
        for child in self.children:
            child.build_tree(node)
        return node
    
    def set_child_amount(self, key, amount):
        for child in self.children:
            if isinstance(child, Line) and child.key == key:
                child.amount = amount
                return True
            elif isinstance(child, Folder) and child.set_child_amount(key, amount) == True:
                 return True
        return False
    
    def _render_name(self):
        return f'[blue bold]{self.name}[/]'