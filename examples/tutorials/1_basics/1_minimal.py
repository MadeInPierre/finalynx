"""
Finalynx - Tutorial 1 - Minimal configuration
=============================================


This tutorial shows how to create the smallest valid portfolio
configuration with a single line.


Try it out by running:
> python3 examples/tutorials/1_minimal.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder # ignore this line, used for git automation
from finalynx import Assistant, Portfolio


# Create a portfolio definition (empty for now), this will be your custom
# structure later on. See the next tutorials for more details.
portfolio = Portfolio()


# Run the assistant to fetch your investments from Finary and add them to your portfolio
# Optionally, set the `ignore_orphans` option to True to ignore investments that are not
# in your portfolio definition. Otherwise, they will be added to the portfolio root:
Assistant(portfolio, ignore_orphans=True).run()  # Default is False
