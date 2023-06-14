from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from finalynx.config import DEFAULT_CURRENCY
from finalynx.config import get_active_theme as TH
from finalynx.portfolio.envelope import Envelope
from finalynx.portfolio.folder import Folder
from finalynx.portfolio.folder import FolderDisplay
from finalynx.portfolio.folder import Portfolio
from finalynx.portfolio.folder import SharedFolder
from finalynx.portfolio.node import Node
from finalynx.portfolio.targets import Target
from rich.tree import Tree


# TODO Generate recommendations as a list of Transaction objects to make, then render them


def render_recommendations(portfolio: Portfolio, envelopes: List[Envelope]) -> Tree:
    """Sort lines with non-zero deltas by envelopes and display them as a summary of transfers to make.
    Call either run() or initialize() first.
    """
    dict_envs: Dict[str, Any] = {}

    # Guide the user to set envelopes if not already done
    if not envelopes:
        return Tree(
            f"[dim {TH().TEXT}]"
            "To activate recommendations, set\n"
            "envelopes to your lines and give\n"
            "them to Assistant (tutorial #11)"
        )

    # Find all folders with non-zero deltas and non-zero amounts (to avoid empty shared folders)
    def _get_folders(node: Folder) -> List[Folder]:
        found: List[Folder] = []
        for child in node.children:
            if isinstance(child, SharedFolder):
                if child.get_amount() > 0:
                    found.append(child)
            elif isinstance(child, Folder):
                if child.display == FolderDisplay.EXPANDED:
                    found += _get_folders(child)
                else:
                    found.append(child)
        return found

    # Check if a folder has non-zero deltas to be displayed in the recommendations
    def _check_node(node: Node) -> bool:
        return node.get_delta() != 0 and node.target.check() not in [
            Target.RESULT_NONE,
            Target.RESULT_OK,
            Target.RESULT_TOLERATED,
        ]

    # Render each envelope of folder's parent with a custom style along with the
    def _render_title(children: List[Any], name: str) -> Tuple[int, str]:
        total_delta = round(sum([c.get_delta() for c in children]))
        return total_delta, (
            f"[{TH().DELTA_POS if total_delta > 0 else TH().DELTA_NEG}]"
            f"{'+' if total_delta > 0 else ''}{total_delta} {DEFAULT_CURRENCY} "
            f"[{TH().FOLDER_COLOR} {TH().FOLDER_STYLE}]{name}[/]"
        )

    # For each envelope, find all lines with non-zero deltas
    for envelope in envelopes:
        if lines := [line for line in envelope.lines if _check_node(line)]:
            delta, title = _render_title(lines, envelope.name)
            dict_envs[title] = (delta, lines)

    # Render folders with non-zero deltas, classify them by parent name
    if folders := [f for f in _get_folders(portfolio) if _check_node(f)]:
        for parent_name in {f.parent.name for f in folders if f.parent}:
            items = [f for f in folders if f.parent and f.parent.name == parent_name]
            delta, title = _render_title(items, parent_name)
            dict_envs[title] = (delta, items)

    # Render the tree with folders containing lines with non-zero deltas (sorted by delta)
    tree = Tree("Envelopes", hide_root=True, guide_style=TH().TREE_BRANCH)
    dict_sorted = {k: v[1] for k, v in sorted(dict_envs.items(), key=lambda item: item[1][0])}  # type: ignore
    for i_env, envelope_name in enumerate(dict_sorted):
        node = tree.add(envelope_name)
        for i_line, line in enumerate(dict_sorted[envelope_name]):
            render = f"[{TH().TEXT}]{line._render_delta(children=dict_sorted[envelope_name])}{line._render_name()}"  # type: ignore
            newline = bool(i_line == len(dict_sorted[envelope_name]) - 1 and i_env < len(dict_envs.keys()) - 1)
            node.add(render + ("\n" if newline else ""))

    # If no envelopes are displayed, show a nice message instead
    if not tree.children:
        tree.add("You're on track! 🎉")
    return tree
