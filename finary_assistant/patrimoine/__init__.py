from ..console import console
from .folder import Folder
from .line import Line
from .node import Node
from .hierarchy import Hierarchy
from .targets import *
from .bucket import Bucket, SharedFolder

# Enable rich's features
from rich import print, inspect, pretty, traceback
from rich.tree import Tree
traceback.install()
pretty.install()

'''
Module: patrimoine
Objectives: 
    - Build a tree of folders to organize a list of investment lines

'''