from typing import Optional


class Hierarchy:
    def __init__(self, parent: Optional["Hierarchy"] = None):
        self.parent = parent

    def set_parent(self, parent: "Hierarchy") -> None:
        self.parent = parent
