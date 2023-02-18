"""
Finary Assistant is a tool to organize your investments in a custom hierarchy, 
fetch real-time values using Finary API, set targets, and simulate your 
portfolio evolution with optional life events and portfolio operations.

This module is maintained by MadeInPierre.
You can always get the latest version of this module at:
    https://github.com/madeinpierre/finary_assistant
"""

__version__ = "1.0.0"
__author__ = "MadeInPierre"
__copyright__ = """
Copyright (c) 2023, MadeInPierre
Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee or royalty is hereby
granted, provided that the above copyright notice appear in all copies
and that both that copyright notice and this permission notice appear
in supporting documentation or portions thereof, including
modifications, that you make.
"""

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
