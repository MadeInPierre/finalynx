"""
DOCUMENTATION
- See available colors: https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors
- See available styles: https://rich.readthedocs.io/en/stable/style.html
"""
from dataclasses import dataclass
from typing import Dict
from typing import Type


@dataclass
class Theme:
    # Main elements
    TEXT = "black"  # Line names, descriptions, default color
    ACCENT = "deep_sky_blue2"  # Elements that must be highlighted (e.g. performances, goal amounts, ...)

    # Main tree elements
    HINT = "dim white"  # Target descriptions and line relative percentage
    FOLDER_COLOR = "dodger_blue2"  # Folders (color only) when in expanded or collapsed display mode
    FOLDER_STYLE = "bold"  # Folders style (no color here) when in expanded mode only
    ENVELOPE_CODE = "dim white"  # Account abbreviation shown right before the line name

    # Targets
    TARGET_NONE = "black"  # No target defined
    TARGET_START = "cyan"  # 0€/$ for this line, start investing!
    TARGET_OK = "green"  # Current amount is with the target
    TARGET_TOLERATED = "yellow"  # Current amount is in the tolerated zone defined in the target
    TARGET_NOK = "red"  # Current amount is outside the target (default)
    TARGET_INVEST = "red"  # Current amount is outside the target, finalynx recommends to invest
    TARGET_DEVEST = "magenta"  # Current amount is outside the target, finalynx recommends to sell

    # Deltas
    DELTA_POS = "green"  # Invest x€/$ to reach the ideal amount defined by the targets
    DELTA_NEG = "red"  # Sell x€/$ to reach the ideal amount defined by the targets
    DELTA_OK = "green"  # Node is already at the perfect amount

    # Decorations
    TREE_BRANCH = "grey42"  # Tree structure color, see rich Tree for additional styles
    PANEL = "black"  # Panel title and border colors


# Shortcut for a more intuitive usage
LightTheme = Theme


@dataclass
class DarkTheme(Theme):
    TEXT = "white"
    HINT = "dim white"
    ENVELOPE_CODE = "dim white"
    TARGET_NONE = "white"
    PANEL = "white"


# List predefined themes, used by `Assistant` to search for class definitions
AVAILABLE_THEMES: Dict[str, Type[Theme]] = {
    "light": LightTheme,
    "dark": DarkTheme,
}
