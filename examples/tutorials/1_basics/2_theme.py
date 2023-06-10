"""
Finalynx - Tutorial 2 - Change the console color theme
======================================================


This tutorial shows how to change the console color theme if
your terminal doesn't have a white background (default theme)
or different color aliases.


Try it out by running:
> python3 examples/tutorials/2_theme.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio
from finalynx import Theme, DarkTheme, LightTheme  # noqa


""" [CUSTOM THEME] ------------------------------------------------------------
Optionally, you can create your own theme by inheriting from Theme.
See the source code of Theme for the list of available settings in
the online documentation. Color names are the same as in Rich, see
> https://rich.readthedocs.io/en/latest/style.html#color-names
"""


class MyCustomTheme(Theme):
    TEXT = "dim red"
    HINT = "bright black"
    ACCENT = "italic bold magenta"
    FOLDER_COLOR = "cyan"
    TARGET_NONE = "dodger_blue2"


# Create a portfolio definition (empty for now) and run the assistant
# with your own theme or one of the pre-built LightTheme() or DarkTheme():
Assistant(Portfolio(), theme=MyCustomTheme()).run()


""" [COMMAND LINE] ------------------------------------------------------------
You can also set the theme from the command line (pre-built themes only):
"""
# > python your_config.py --theme=dark
# > python your_config.py -t dark
