from typing import Any
from typing import Dict

import finalynx.portfolio.folder as folder
import finalynx.portfolio.line as line
import finalynx.portfolio.node as node
import finalynx.portfolio.shared_folder as shared_folder


def node_from_dict(dict: Dict[str, Any]) -> node.Node:
    if "type" not in dict:
        raise ValueError("Expected node, must have 'type' key.")
    elif dict["type"] == "line":
        return line.Line.from_dict(dict)
    elif dict["type"] == "folder":
        return folder.Folder.from_dict(dict)
    elif dict["type"] == "shared_folder":
        return shared_folder.SharedFolder.from_dict(dict)
    else:
        raise ValueError("Unrecognized node type.")
