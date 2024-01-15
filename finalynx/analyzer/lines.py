from typing import Any
from typing import Dict

from ..portfolio import Folder
from ..portfolio import Line
from ..portfolio import Node
from .analyzer import Analyzer


class AnalyzeLines(Analyzer):
    """Aims to agglomerate the children's pf lines and return
    the amount represented by each line.
    :returns: a dictionary with lines as keys and the
    corresponding total amount contained in the children.
    """

    def analyze(self) -> Dict[str, float]:
        """:returns: A dictionary with keys as the asset class names and values as the
        sum of investments corresponding to each class."""
        return self._recursive_merge(self.node)

    def _recursive_merge(self, node: Node) -> Dict[str, Any]:
        """Internal method for recursive searching."""
        total = {}

        # Lines simply return their own amount
        if isinstance(node, Line):
            if node.name:
                total[node.name] = node.get_amount()
            else:
                total["Unknown"] = node.get_amount()
            return total

        # Folders merge what the children return
        elif isinstance(node, Folder):
            for child in node.children:
                for key, value in self._recursive_merge(child).items():
                    if key in total.keys():
                        total[key] += value
                    else:
                        total[key] = value
            return total

        # Safeguard for future versions
        else:
            raise ValueError(f"Unknown node type '{type(node)}'.")
