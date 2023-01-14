from .simulator import Simulator

# Enable rich's features
from rich import print, inspect, pretty, traceback
from rich.tree import Tree
traceback.install()
pretty.install()