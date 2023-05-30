"""
This file is where Finalynx's overall behavior can be customized.
"""
from .theme import LightTheme
from .theme import Theme

# When the currency symbol is not specified in the user config, use this symbol
DEFAULT_CURRENCY = "€"

# Hold the active theme used, defaults to light theme
_active_theme: Theme = LightTheme()


def set_active_theme(theme: Theme) -> None:
    """Setter method needed to pass elements by reference accross modules."""
    global _active_theme
    _active_theme = theme


def get_active_theme() -> Theme:
    """Getter method needed to pass elements by reference accross modules."""
    return _active_theme
