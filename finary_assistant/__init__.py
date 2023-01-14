from .patrimoine import console
from .patrimoine import Folder
from .patrimoine import Line
from .patrimoine import Node
from .patrimoine import Hierarchy
from .patrimoine import Bucket, SharedFolder
from .patrimoine import TargetRange, TargetMin, TargetMax, TargetRatio, TargetGlobalRatio

from .fetch import finary_fetch

# Enable rich's features
from rich import print, inspect, pretty, traceback
from rich.tree import Tree
traceback.install()
pretty.install()