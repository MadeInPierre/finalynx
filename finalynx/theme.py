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
    ENVELOPE_CODE = "dim white"  # TODO?

    # Targets
    TARGET_NONE = TEXT
    TARGET_START = "cyan"
    TARGET_OK = "green"
    TARGET_NOK = "red"
    TARGET_TOLERATED = "yellow"
    TARGET_INVEST = "red"
    TARGET_DEVEST = "magenta"

    # Deltas
    DELTA_POS = "green"
    DELTA_NEG = "red"
    DELTA_OK = DELTA_POS

    # Decorations
    TREE_BRANCHES = "grey42"
    PANEL = TEXT


# Shortcut for a more intuitive usage
LightTheme = Theme


@dataclass
class DarkTheme(Theme):
    TEXT = "white"


# List predefined themes, used by `Assistant` to search for class definitions
AVAILABLE_THEMES: Dict[str, Type[Theme]] = {
    "light": LightTheme,
    "dark": DarkTheme,
}
