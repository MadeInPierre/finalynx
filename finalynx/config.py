"""
This file is where Finalynx's overall behavior can be customized.
"""
from .theme import LightTheme
from .theme import Theme

# When the currency symbol is not specified in the user config, use this symbol
DEFAULT_CURRENCY = "€"

# Hold the active theme used, defaults to light theme
ACTIVE_THEME: Theme = LightTheme()
