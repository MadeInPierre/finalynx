from typing import Optional


class Hierarchy:
    """Abstract class for objects that hold their parent's reference in a tree."""

    def __init__(self, parent: Optional["Hierarchy"] = None):
        """:param parent: The parent's reference."""
        self.parent = parent

    def set_parent(self, parent: "Hierarchy") -> None:
        """:param parent: The reference of the new parent."""
        self.parent = parent
