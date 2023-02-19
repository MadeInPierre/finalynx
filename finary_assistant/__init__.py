"""
Finary Assistant is a tool to organize your investments in a custom hierarchy, 
fetch real-time values using Finary API, set targets, and simulate your 
portfolio evolution with optional life events and portfolio operations.

This module is maintained by MadeInPierre.
You can always get the latest version of this module at:
    https://github.com/madeinpierre/finary_assistant
"""


# Import meta information such as version, author, copyright, etc.
from __meta__ import *

import os
import sys

# add finary_api submodule to path to allow imports to work
sys.path.append(os.path.join(os.path.dirname(__file__), "finary_api"))

# Portfolio
from .portfolio import TargetRange, TargetMin, TargetMax, TargetRatio, TargetGlobalRatio
from .portfolio import Line, Folder, Bucket, SharedFolder, Portfolio, FolderDisplay
from .portfolio import console

# Fetch
from .fetch import finary_fetch

# Advisor
from .copilot import Copilot

# Simulator
from .simulator import Simulator

# Main
from .assistant import Assistant

# Enable rich's features
from rich import print, inspect, pretty, traceback
from rich.tree import Tree

traceback.install()
pretty.install()
