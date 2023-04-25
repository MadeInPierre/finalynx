from typing import Any
from typing import Dict
from typing import Optional

import numpy as np

from .bucket import Bucket
from .constants import AssetClass
from .folder import Folder
from .folder import FolderDisplay
from .line import Line
from .targets import Target


class SharedFolder(Folder):
    def __init__(
        self,
        name: str,
        bucket: Bucket,
        asset_class: AssetClass = AssetClass.UNKNOWN,
        target_amount: float = np.inf,
        parent: Optional["Folder"] = None,
        target: Optional["Target"] = None,
        newline: bool = False,
        display: FolderDisplay = FolderDisplay.EXPANDED,
    ):
        super().__init__(name, asset_class, parent, target, bucket.lines, newline=False, display=display)  # type: ignore # TODO couldn't fix the mypy error
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
                child.amount = amount
                success = True
            elif isinstance(child, Folder) and child.set_child_amount(key, amount):
                success = True
        return success

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
    def from_dict(dict: Dict[str, Any]) -> "SharedFolder":
        return SharedFolder(
            name=dict["name"],
            bucket=Bucket(dict["bucket_name"], []),  # TODO
            target_amount=dict["target_amount"],
            target=Target.from_dict(dict["target"]),
            newline=bool(dict["newline"]),
            display=FolderDisplay(dict["display"]),
        )
