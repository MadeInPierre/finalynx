"""
```{tip}
This subpackage has a [dedicated milestone](https://github.com/MadeInPierre/finalynx/milestones?direction=asc&sort=title&state=open) in the development steps.
```

This is the core subpackage of Finalynx. It defines the Portfolio tree, folders and line objects, targets, and buckets for each node in the tree.

Here is a quick help to navigate this subpackage:
- `Hierarchy` is the base abstract class for classes that hold references to their parents (`Node` and `Target` classes).
    - `Node` is an abstract class to define a level in the tree that adds a name and target. It has the following subclasses:
        - `Line` represents a single investment line in your Finary account. It adds an amount which is fetched from Finary.
        - `Folder` adds a list of children and additional rendering logic to generate the console output.
            - `SharedFolder` takes a single `Bucket` as input and uses its superclass' list of children to hold the lines from the bucket.
            It adds a target amount that defines how much to take from the bucket before letting the other shared folders use what's left.
            - `Portfolio` is nothing more than a simple renaming of `Folder` for user clarity.
- `Bucket` is a list of `Line` objects with additional logic to let shared folders use a portion of the total amount.
- `Target` is an abstract class that defines a common logic and console rendering for all subclasses. Checkout the submodule to see which targets
are available.

% TODO
```{note}
`constants` is not used for now, but may soon be the basis of future `Envelope` objects.
```
"""
# flake8: noqa
from ..console import console
from .bucket import Bucket
from .constants import AssetClass
from .constants import AssetSubclass
from .constants import EnvelopeClass
from .envelope import *
from .folder import Folder
from .folder import FolderDisplay
from .folder import Portfolio
from .folder import SharedFolder
from .hierarchy import Hierarchy
from .line import Line
from .line import LinePerf
from .node import Node
from .targets import *
