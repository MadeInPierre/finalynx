"""
Finalynx - Tutorial 5 - Change some simple display options
==========================================================

This tutorial shows how to customize the rendering of your portfolio
as well as the console output.

Try it out by running:
> python3 examples/tutorials/5_display_options.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio


""" [HIDE AMOUNTS] ------------------------------------------------------------
Optionally, you can hide the amounts of your investments by setting the
`hide_amounts` option to True. This is useful if you want to share your
portfolio with someone else without revealing the amounts.
"""


""" [HIDE ROOT] ---------------------------------------------------------------
Optionally, you can hide the root of your portfolio by setting the
`hide_root` option to True. This is simply an aesthetic preference.
"""


""" [SHOW DATA] ---------------------------------------------------------------
When Finalynx fetches your data from Finary and other sources, it creates a
data structure that can be displayed in the console. This is useful to make
sure that the data is correct and to debug any issues. By default, this data
is hidden but you can change this by setting the `show_data` option to True.
"""


# Create a portfolio definition (empty for now)
portfolio = Portfolio()

# Run the assistant with the `hide_amounts`, `hide_root` or `show_data` options:
Assistant(
    portfolio,
    hide_amounts=True,  # Replace real amounts with dots, defaults to False
    hide_root=True,  # Hide the Portfolio root (aesthetic preference), defaults to False
    show_data=True,  # Show the data fetched from Finary (and other sources), defaults to False
    clear_cache=True,  # Used in this tutorial only to make sure you see something cool when you run it
).run()


""" [COMMAND LINE] ------------------------------------------------------------
You can also control these from the command line:
"""
# > python your_config.py -a (same as --hide-amounts)
# > python your_config.py -r (same as --hide-root)
# > python your_config.py -d (same as --hide-data)
