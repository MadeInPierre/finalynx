"""This file defines elements used to match `Line` instances defined in the main portfolio
tree with investments fetched online (e.g. from your Finary account).
"""
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import numpy as np
from finalynx.console import console
from finalynx.portfolio.node import Node


@dataclass
class FetchAttribs:
    """Abstract class that defines common attributes used to match Keys (defined in the portfolio)
    with FetchLines (created by fetch agents, e.g. `FinaryFetch`)."""

    name: Optional[str] = None
    id: Optional[str] = None
    account: Optional[str] = None
    custom: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Runs after an instance is created to validate inputs. At least one field must be set."""
        if not (self.name or self.id or self.account or self.custom):
            raise ValueError(f"{type(self).__name__} instance must have at least one field set.")


@dataclass
class FetchLine(FetchAttribs):
    """Represents each investment found in your online accounts (e.g. Finary). The instance is
    populated with information found online about this line. FetchLines will then be matched to Keys
    defined in the portfolio to populate 'real' `Line` instances with FetchLine information."""

    amount: float = 0
    currency: Optional[str] = None


@dataclass
class FetchKey(FetchAttribs):
    """Represents a filter to match an investment fetch online (e.g. from your Finary account)
    to a `Node` in your portfolio tree. At least one of the available fields must be set.

    :param match_all: Only match with a `FetchLine` if all fields are the same, defaults to
    False (meaning any matched fields will procude a full match).
    :param parent: Used internally to link a key with its parent and share attributes.
    """

    match_all: bool = False
    parent: Optional[Node] = None

    def set_parent(self, node: Node) -> None:
        """Used by each Node's initialization stage to link its own properties."""
        self.parent = node

    def match(self, fetch_line: FetchLine) -> bool:
        """:returns: True if any (or all if specified) of"""
        pairs = [
            (self.parent.name if self.parent else None, fetch_line.name),
            (self.name, fetch_line.name),
            (self.id, fetch_line.id),
            (self.account, fetch_line.account),
        ]

        # Add the common custom attributes to the comparison
        if self.custom and fetch_line.custom:
            for key in self.custom.keys():
                if key in fetch_line.custom.keys():
                    pairs.append((self.custom[key], fetch_line.custom[key]))

        # Compare all pairs, use None if one of the values is None
        results: List[Optional[bool]] = [
            (None if (value1 is None or value2 is None) else (value1 == value2)) for value1, value2 in pairs
        ]

        # Safety check, make sure at least one pair wasn't (None, None)
        if len([i for i in results if i is None]) == len(results):
            console.log("[yellow][bold]Warning:[/] Key couldn't compare with any of the fetched line's attributes.")
            return False

        # This method reaches here if all compared pairs matched (or if no pair could be compared)
        return bool(np.all([i for i in results if i is not None])) if self.match_all else bool(True in results)
