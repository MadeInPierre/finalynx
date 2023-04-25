# from typing import Any
# from typing import Dict
from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from .folder import Folder
from .targets import Target

# from finalynx.parse.node_from_dict import node_from_dict


if TYPE_CHECKING:
    from .node import Node


class Portfolio(Folder):
    """This is the root of your custom portfolio hierarchy."""

    def __init__(
        self, name: str = "Portfolio", target: Optional["Target"] = None, children: Optional[List["Node"]] = None
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
        super().__init__(name, parent=None, target=target, children=children, newline=False)

    # @staticmethod
    # def from_dict(dict: Dict[str, Any]) -> "Portfolio":
    #     return Portfolio(
    #         name=dict["name"],
    #         target=Target.from_dict(dict["target"]),
    #         children=[node_from_dict(c) for c in dict["children"]],
    #     )
