from enum import Enum
from typing import Any
from typing import List
from typing import Optional
from typing import TYPE_CHECKING

import numpy as np
from finalynx.console import console
from finalynx.portfolio.targets import TargetRatio
from rich.tree import Tree

from .constants import AssetClass
from .line import Line
from .node import Node

if TYPE_CHECKING:
    from .targets import Target


class FolderDisplay(Enum):
    """Enumeration to select how a folder should be displayed.

    There are three options:
    - **Expanded:** Show all children in the output.
    - **Collapsed:** Only show the folder name.
    - **Line:** Only show the folder name and render it as if it was a line.
    """

    EXPANDED = 0
    COLLAPSED = 1
    LINE = 2


class Folder(Node):
    """Holds a group of `Node` objects to build the portfolio hierarchy."""

    def __init__(
        self,
        name: str,
        asset_class: AssetClass = AssetClass.UNKNOWN,
        parent: Optional["Folder"] = None,
        target: Optional["Target"] = None,
        children: Optional[List["Node"]] = None,
        newline: bool = False,
        display: FolderDisplay = FolderDisplay.EXPANDED,
    ):
        """
        This class handles the orchestration of rendering of its children.

        :param name: Name to be displayed in the final output.
        :param parent: Optional Node object as a parent. Each folder sets their children's
        parents as itself by default.
        :param target: Optional `Target` instance for this folder to render the total amount
        based on your own investment objectives.
        :param children: List of `Node` objects contained in the folder. The folder's amount
        corresponds to the sum of the amounts contained in all children.
        :param newline: When printing to the console, you can print a blank line after this folder
        for better readability.
        :param display: Choose how the folder should be displayed (expanded, collapsed or as a line).
        """
        super().__init__(name, parent, target, newline)
        self.children = [] if children is None else children
        self.display = display

        for child in self.children:
            child.set_parent(self)

        self.set_children_class(asset_class)

    def add_child(self, child: Node) -> None:
        """Manually add a child at the end of the existing children in this folder.
        :param child: Any `Node` object to add as a child.
        :returns: Nohing to return.
        """
        child.set_parent(self)
        self.children.append(child)

    def get_amount(self) -> float:
        """Get the total amount contained in this folder.
        :returns: The sum of what each child's `get_amount()` method returns.
        """
        return float(np.sum([child.get_amount() for child in self.children]) if self.children else 0)

    def tree(
        self,
        output_format: str = "[console]",
        _tree: Optional[Tree] = None,
        hide_root: bool = False,
        **render_args: Any,
    ) -> Tree:
        """Generate a fully rendered `Tree` object from the `rich` package using the

        This `Tree` can either be manipulated for further operations or directly printed
        to the console using rich's `print` method.

        :param hide_amount: Replace the amoutns by simple dots (easier to share the result), defaults to False.
        :param _tree: Internal method to pass the folder's root tree object to the children.
        :param args: Provide any list of arguments supported by the `Tree` class if this is the root folder in the hierarchy.
        :param format: `rich` for console output, `name` for only names, defaults to `rich`
        :returns: A `Tree` instance containing the rendered titles for each `Node` object.
        """
        render = self.render(output_format, **render_args)
        node = _tree.add(render) if _tree else Tree(render, guide_style="grey42", hide_root=hide_root)
        if self.display == FolderDisplay.EXPANDED:
            for child in self.children:
                child.tree(output_format=output_format, _tree=node, **render_args)
        return node

    def process(self) -> None:
        """Some `Node` or `Target` objects might need to process some data once the investment
        values have been fetched from Finary. Folders do not have any processing procedure.
        Here, we only call the `process()` method of all children.
        """
        total_ratio = 0.0

        for child in self.children:
            child.process()

            if isinstance(child.target, TargetRatio):
                total_ratio += child.target.target_ratio

        if total_ratio != 0 and total_ratio != 100:
            console.log(f"[yellow][bold]WARNING:[/] Folder '{self.name}' total ratio should sum to 100.")

    def set_child_amount(self, key: str, amount: float) -> bool:
        """Used by the `fetch` subpackage to

        This method passes down the vey:value pair corresponding to an investment fetched online
        (e.g. in your Finary account) to its children until a match is found.

        :param key: Name of the line in the online account.
        :param amount: Fetched amount in the online account.
        """
        success = False
        for child in self.children:
            if isinstance(child, Line) and child.key == key:
                child.amount += amount
                success = True
            elif isinstance(child, Folder) and child.set_child_amount(key, amount):
                success = True
        return success

    def set_children_class(self, asset_class: AssetClass) -> None:
        for child in self.children:
            if isinstance(child, Line):
                child.asset_class = asset_class if child.asset_class is AssetClass.UNKNOWN else child.asset_class
            elif isinstance(child, Folder):
                child.set_children_class(asset_class)
            else:
                raise ValueError("Unrecognized node type.")

    def _render_name_color(self) -> str:
        """Internal method that overrides the superclass' render method to display
        the folder name with a bold font of different color.
        """
        if self.display == FolderDisplay.EXPANDED:
            return "[dodger_blue2 bold]"
        elif self.display == FolderDisplay.COLLAPSED:
            return "[dodger_blue2]"
        elif self.display == FolderDisplay.LINE:
            return super()._render_name_color()
        else:
            raise ValueError("Display mode '{self.display}' not recognized.")

    def _render_newline(self) -> str:
        """Internal method that overrides the superclass' render method to display
        a new line after the folder has rendered.
        :returns: The newline character depending on the user configuration.
        """
        return "\n" if self.newline and self.display != FolderDisplay.EXPANDED else ""
