"""
Finalynx - Tutorial 10 - Set investment targets for your lines
==============================================================

This tutorial shows how to define investment targets for your lines. For each node
in the portfolio tree, you can set various types of targets to help you reach your
investment goals. These targets include:
- `TargetRange`: a range of values that you want to reach for a given line.
- `TargetMin` and `TargetMax`: a minimum and maximum value that you want to maintain.
- `TargetRatio`: a ratio that this `Node` must represent in the parent `Folder`.
- `TargetGlobalRatio`: a ratio that this `Node` must represent in the entire portfolio.


See the online documentation for the list of available targets:
> https://github.com/MadeInPierre/finalynx/blob/main/finalynx/portfolio/targets.py

Try it out by running:
> python3 examples/tutorials/10_targets.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio, Folder, Line
from finalynx import TargetRange, TargetMin, TargetMax, TargetRatio, TargetGlobalRatio


""" [TARGETS] -----------------------------------------------------------------
Use the `target` argument to set a target for a line of folder. In this example,
fake `amount` values are simply used to show a nice result if you run this code.
"""


portfolio = Portfolio(
    "My Portfolio",  # Only used for display purposes
    children=[
        # Notify me if this line goes above 500
        Line("Neobank", amount=400, target=TargetMax(500)),
        # Target a range of values
        Line("Bank account", amount=1200, target=TargetRange(1000, 2000)),
        # Add a tolerance so that Finalynx tolerates 1500 € for this line (displays line in yellow):
        Line("Savings for travels", amount=1800, target=TargetMin(2000, tolerance=500)),
        Folder(
            "Stocks",
            # Target a ratio of 60% for this folder (relative to the total amount in the parent folder)
            target=TargetRatio(60),
            children=[
                # Zone is the tolerance around the target ratio to get a green color, defaults to 4%
                Line("Line 1", amount=2000, target=TargetRatio(50, zone=2)),
                # Tolerance is the tolerance around the target ratio + zone to get a yellow color, defaults to 2%
                Line("Line 2", amount=2500, target=TargetRatio(30, tolerance=4)),
                # This line is green at 19-21% and yellow at 9-31%
                Line("Line 3", amount=3000, target=TargetRatio(20, zone=1, tolerance=10)),
            ],
        ),
        Folder(
            "Real estate",
            target=TargetGlobalRatio(40),
            children=[
                Line("Line 4", amount=1300),
            ],
        ),
    ],
)


# Run the assistant (ignore_orphans is used to make the result nicer when you run this tutorial):
Assistant(portfolio, ignore_orphans=True).run()
