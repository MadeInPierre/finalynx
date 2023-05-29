from dataclasses import dataclass
from typing import Dict
from typing import Type


@dataclass
class Theme:
    # Main elements
    DEFAULT_TEXT = "black"
    HINT = "dim white"

    # Folders
    FOLDER_COLOR = "blue"
    FOLDER_STYLE = "bold"

    # Targets
    TARGET_NONE = "green"
    TARGET_OK = "green"
    TARGET_NOK = "red"
    TARGET_TOLERATED = "yellow"


# Shortcut for a more intuitive usage
LightTheme = Theme


@dataclass
class DarkTheme(Theme):
    DEFAULT_TEXT = "white"


# List predefined themes, used by `Assistant` to search for class definitions
AVAILABLE_THEMES: Dict[str, Type[Theme]] = {
    "light": LightTheme,
    "dark": DarkTheme,
}
