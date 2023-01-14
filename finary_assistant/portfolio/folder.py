import numpy as np
from rich.tree import Tree
from .node import Node
from .line import Line


class Folder(Node):
    def __init__(self, name, parent=None, target=None, children=None, newline=False):
        super().__init__(name, parent, target, newline=False)
        self.children = [] if children is None else children

        for child in self.children:
            child.set_parent(self)
        
        if self.children:
            child.newline = newline
    
    def add_child(self, child):
        child.set_parent(self)
        self.children.append(child)
    
    def get_amount(self):
        return np.sum([child.get_amount() for child in self.children]) if self.children else 0

    def build_tree(self, tree=None, **args):
        node = Tree(str(self), guide_style='grey42', **args) if tree is None else tree.add(str(self))
        for child in self.children:
            child.build_tree(node)
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
            elif isinstance(child, Folder) and child.set_child_amount(key, amount) == True:
                success = True
        return success
    
    def _render_name(self):
        return f'[blue bold]{self.name}[/]'
    
    def _render_newline(self):
        return ''