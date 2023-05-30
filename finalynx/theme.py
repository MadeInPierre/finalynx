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
    TEXT = "black"
    ACCENT = "deep_sky_blue2"

    # Main tree elements
    HINT = "dim white"
    FOLDER_COLOR = "dodger_blue2"
    FOLDER_STYLE = "bold"
    ENVELOPE_CODE = "dim white"

    # Targets
    TARGET_NONE = "black"
    TARGET_START = "cyan"
    TARGET_OK = "green"
    TARGET_NOK = "red"
    TARGET_TOLERATED = "yellow"
    TARGET_INVEST = "red"
    TARGET_DEVEST = "magenta"

    # Deltas
    DELTA_POS = "green"
    DELTA_NEG = "red"
    DELTA_OK = "green"

    # Decorations
    TREE_BRANCHES = "grey42"
    PANEL = "black"


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
