from .node import Node


class Line(Node):
    def __init__(
        self, name, parent=None, target=None, key=None, amount=0, newline=False
    ):
        super().__init__(name, parent, target, newline)
        self.key = key if key is not None else name
        self.amount = amount

    def get_amount(self):
        return self.amount
