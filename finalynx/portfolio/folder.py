from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import TYPE_CHECKING

import numpy as np
from rich.tree import Tree

if TYPE_CHECKING:
    from finalynx.fetch.fetch_line import FetchLine

from ..console import console
from .bucket import Bucket
from .constants import AssetClass
from .constants import AssetSubclass
from .envelope import Envelope
from .line import Line
from .line import LinePerf
from .node import Node
from .targets import Target
from .targets import TargetRatio


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
        asset_subclass: AssetSubclass = AssetSubclass.UNKNOWN,
        parent: Optional["Folder"] = None,
        target: Optional["Target"] = None,
        children: Optional[List["Node"]] = None,
        newline: bool = False,
        display: FolderDisplay = FolderDisplay.EXPANDED,
        perf: Optional[LinePerf] = None,
        currency: Optional[str] = None,
        envelope: Optional[Envelope] = None,
    ):
        """
        This class handles the orchestration of rendering of its children.

        :param name: Name to be displayed in the final output.
        :param asset_class: Useful shortcut to set all chidlren's asset class at once. Children keep priority
        over this shortcut.
        :param parent: Optional Node object as a parent. Each folder sets their children's
        parents as itself by default.
        :param target: Optional `Target` instance for this folder to render the total amount
        based on your own investment objectives.
        :param children: List of `Node` objects contained in the folder. The folder's amount
        corresponds to the sum of the amounts contained in all children.
        :param newline: When printing to the console, you can print a blank line after this folder
        for better readability.
        :param display: Choose how the folder should be displayed (expanded, collapsed or as a line).
        :param perf: Useful shortcut to set all chidlren's performance at once. Children keep priority
        over this shortcut.
        """
        super().__init__(name, parent, target, newline)
        self.children = [] if children is None else children
        self.display = display
        self.asset_class = asset_class
        self.asset_subclass = asset_subclass
        self.perf = perf
        self.currency = currency
        self.envelope = envelope

        for child in self.children:
            child.set_parent(self)

            self.set_child_attribs(
                child,
                self.asset_class,
                self.asset_subclass,
                self.perf,
                self.currency,
                self.envelope,
            )

    def add_child(self, child: Node) -> None:
        """Manually add a child at the end of the existing children in this folder.
        :param child: Any `Node` object to add as a child.
        :returns: Nohing to return.
        """
        child.set_parent(self)
        self.children.append(child)
        self.set_child_attribs(child, self.asset_class, self.asset_subclass, self.perf, self.currency, self.envelope)

    def get_amount(self) -> float:
        """Get the total amount contained in this folder.
        :returns: The sum of what each child's `get_amount()` method returns.
        """
        return float(np.sum([child.get_amount() for child in self.children]) if self.children else 0)

    def get_currency(self) -> str:
        """:returns: This folder's currency symbol, equal to its children common currency.
        If children have different currencies, return an unknown symbol (TODO to be improved)."""
        currencies = [c.get_currency() for c in self.children]
        if currencies and currencies.count(currencies[0]) == len(currencies):
            return currencies[0]
        return "#"  # TODO replace with a better behavior

    def get_ideal(self) -> float:
        """:returns: The ideal amount to be invested in this node based on surrounding targets."""
        return (
            self.target.get_ideal()
            if self.target.check() != Target.RESULT_NONE
            else float(np.sum([c.get_ideal() for c in self.children]))
        )

    def get_perf(self, ideal: bool = True) -> LinePerf:
        """Get the weighted mean expected performance of all children to get the folder's
        expected performance."""

        # Get children's performances
        children = [c for c in self.children if not (isinstance(c, Line) and c.perf.skip)]
        perfs = [c.get_perf(ideal) if isinstance(c, Folder) else c.get_perf() for c in children]

        # If this folder is empty or all children want to be skipped, mark self as skipped
        if not children or np.all([p.skip for p in perfs]):
            return LinePerf(0, skip=True)

        # Get every not-skipped children's expected amounts (either current or ideal)
        amounts = [(c.get_ideal() if ideal else c.get_amount()) for c in children]
        total = np.sum(amounts)

        # If children have not set targets, give identical weights to each child
        if not total:
            weights = list(np.ones(len(amounts)) / len(amounts))
        else:
            weights = [e / total for e in amounts]

        # Calculate the folder's performance as the weighted sum of not-skipped children's performances
        return LinePerf(np.sum([w * p.expected for w, p in zip(weights, perfs)]))

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

    # TODO convert this to show any customizable output_format?
    def tree_delta(self, _tree: Optional[Tree] = None) -> Tree:
        """Generates a tree with delta amounts to be invested to reach the ideal portfolio allocation."""
        render = self._render_delta(align=False)

        # Follow the same print policy as the main tree
        if self.display != FolderDisplay.EXPANDED and self.newline:
            render += "\n"

        # Add every element to the root to create a flat tree
        if not _tree:
            _tree = Tree(render, hide_root=True)
        else:
            _tree.add(render)

        # Add children if they are displayed in the main tree as well
        if self.display == FolderDisplay.EXPANDED:
            for child in self.children:
                child.tree_delta(_tree=_tree)
        return _tree

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

    def match_lines(self, fetch_line: "FetchLine") -> List[Line]:
        """Used by the `fetch` subpackage to

        This method passes down the instance corresponding to an investment fetched online
        (e.g. in your Finary account) to its children and returns a constructed list of matching lines.

        :param fetch_line: FetchLine instance created that represents an investment found online.
        :returns: A list of nodes that match with the online investment based on name, key, envelope, etc.
        """
        matched: List[Line] = []

        # Automatically match lines with the Folder's envelope
        if self.envelope and fetch_line.account in [self.envelope.key, self.envelope.name]:
            generated_line = fetch_line.generate_line()
            self.add_child(generated_line)
            matched.append(generated_line)

        # Default behavior: return children lines that fully matched
        for child in self.children:
            if isinstance(child, Line) and fetch_line.matches_line(child):
                matched.append(child)
            elif isinstance(child, Folder):
                matched += child.match_lines(fetch_line)
        return matched

    def set_child_attribs(
        self,
        child: Node,
        asset_class: AssetClass,
        asset_subclass: AssetSubclass,
        perf: Optional[LinePerf],
        currency: Optional[str],
        envelope: Optional[Envelope],
    ) -> None:
        """Used by Folders to set attributes once in the Folder instead of setting it in each child.
        Called at initialization time and when a child is manually added to the folder."""
        if isinstance(child, Line):
            child.asset_class = asset_class if child.asset_class == AssetClass.UNKNOWN else child.asset_class
            child.asset_subclass = (
                asset_subclass if child.asset_subclass == AssetSubclass.UNKNOWN else child.asset_subclass
            )
            child.perf = perf if perf and child.perf.expected == 0 else child.perf
            child.currency = currency if currency else child.currency
            child.envelope = envelope if envelope else child.envelope
        elif isinstance(child, Folder):
            for c in child.children:
                child.set_child_attribs(c, asset_class, asset_subclass, perf, currency, envelope)
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

    def _render_ideal(self) -> str:
        """:returns: A string representation of the ideal amount to be invested in
        this folder. If this folder has no target, use the sum of its children's ideals."""
        if self.target.check() != Target.RESULT_NONE:
            return self.target.render_ideal()
        ideal = float(np.sum([c.get_ideal() for c in self.children]))
        return f"{round(ideal)} {self._render_currency()} " if ideal else ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "folder",
            "name": self.name,
            "target": self.target.to_dict(),
            "children": [child.to_dict() for child in self.children],
            "newline": self.newline,
            "display": self.display.value,
        }

    @staticmethod
    def from_dict(dict: Dict[str, Any], buckets: Dict[str, Bucket], envelopes: Dict[str, Envelope]) -> "Folder":
        children: List[Node] = []

        for child_dict in dict["children"]:
            if child_dict["type"] == "line":
                children.append(Line.from_dict(child_dict, envelopes))
            elif child_dict["type"] == "folder":
                children.append(Folder.from_dict(child_dict, buckets, envelopes))
            elif child_dict["type"] == "shared_folder":
                children.append(SharedFolder.from_dict(child_dict, buckets))

        return Folder(
            name=dict["name"],
            target=Target.from_dict(dict["target"]),
            children=children,
            display=FolderDisplay(dict["display"]),
            newline=bool(dict["newline"]),
        )


class SharedFolder(Folder):
    def __init__(
        self,
        name: str,
        bucket: Bucket,
        asset_class: AssetClass = AssetClass.UNKNOWN,
        asset_subclass: AssetSubclass = AssetSubclass.UNKNOWN,
        target_amount: float = np.inf,
        parent: Optional["Folder"] = None,
        target: Optional["Target"] = None,
        newline: bool = False,
        display: FolderDisplay = FolderDisplay.EXPANDED,
    ):
        super().__init__(name, asset_class, asset_subclass, parent, target, bucket.lines, newline=False, display=display)  # type: ignore # TODO couldn't fix the mypy error
        self.target_amount = target_amount
        self.newline = newline
        self.bucket = bucket

    def process(self) -> None:
        super().process()  # Process children
        self.children = self.bucket.use_amount(self.target_amount)  # type: ignore # TODO couldn't fix the mypy error

        for child in self.children:
            child.set_parent(self)

        if self.children:
            self.children[-1].newline = self.newline

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "shared_folder",
            "name": self.name,
            "bucket_name": self.bucket.name,
            "target_amount": self.target_amount,
            "target": self.target.to_dict(),
            "newline": self.newline,
            "display": self.display.value,
        }

    @staticmethod
    def from_dict(dict: Dict[str, Any], buckets: Dict[str, Bucket]) -> "SharedFolder":  # type: ignore
        return SharedFolder(
            name=dict["name"],
            bucket=buckets[dict["bucket_name"]],
            target_amount=dict["target_amount"],
            target=Target.from_dict(dict["target"]),
            newline=bool(dict["newline"]),
            display=FolderDisplay(dict["display"]),
        )


class Portfolio(Folder):
    """This is the root of your custom portfolio hierarchy."""

    def __init__(
        self,
        name: str = "Portfolio",
        target: Optional["Target"] = None,
        children: Optional[List["Node"]] = None,
        currency: Optional[str] = None,
    ):
        """
        This class is actually nothing more than a normal `Folder` renamed to `Portfolio` for user clarity
        (and with 'Portfolio' as the default folder name). Technically, the hierarchy could just as much
        start with a `Folder` object.

        :param name: The name that will be displayed in the rendered tree, defaults to _Portfolio_.
        :param target: optional `TargetSomething` instance to render the total portfolio amount with
         certain conditions, defaults to None.
        :param children: List of `Line`, `Folder`, and `SharedFolder` objects to recursively define the
        entire structure, defaults to an empty list.
        """
        super().__init__(
            name,
            parent=None,
            target=target,
            children=children,
            newline=False,
            currency=currency,
        )

    @staticmethod
    def from_dict(dict: Dict[str, Any], buckets: Dict[str, Bucket], envelopes: Dict[str, Envelope]) -> "Portfolio":
        children: List[Node] = []

        for child_dict in dict["children"]:
            if child_dict["type"] == "line":
                children.append(Line.from_dict(child_dict, envelopes))
            elif child_dict["type"] == "folder":
                children.append(Folder.from_dict(child_dict, buckets, envelopes))
            elif child_dict["type"] == "shared_folder":
                children.append(SharedFolder.from_dict(child_dict, buckets))

        return Portfolio(
            name=dict["name"],
            target=Target.from_dict(dict["target"]),
            children=children,
        )
