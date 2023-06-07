"""
Finalynx - Tutorial 9 - Set custom attributes for your lines
===============================================================

This tutorial shows how to define custom attributes for your lines, which include:
- Asset classes and subclasses are used in the dashboard to display the repartition
  of your investments by asset class with graphs. In the future, they might also
  be used to compute the risk level of your portfolio, recommendations, etc.
- Expected performence can be set to simulate your entire portfolio's present and
  future performance.

See the online documentation for the list of available asset classes & subclasses:
> https://github.com/MadeInPierre/finalynx/blob/main/finalynx/portfolio/constants.py

Try it out by running:
> python3 examples/tutorials/9_asset_classes.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio, Folder, Line
from finalynx import AssetClass, AssetSubclass, LinePerf


""" [ASSET CLASSES & SUBCLASSES] ----------------------------------------------
Use the `asset_class` and `asset_subclass` arguments to set each line type.

You can also set the `asset_(sub)class` of a `Folder` to set the default
`Asset(Sub)Class` of all its children. Note that setting the `asset_(sub)class`
of a `Line` will override the `asset_(sub)class` of its parent `Folder`.
"""


""" [EXPECTED PERFORMANCE] ----------------------------------------------------
Use the `perf` argument to set the expected performance of a line. Just like
the `asset_(sub)class` arguments, you can also set the `perf` of a `Folder`
to set the default `perf` of all its children.
"""


portfolio = Portfolio(
    "My Portfolio",  # Only used for display purposes
    children=[
        # Defaults to AssetClass.UNKNOWN, AssetSubclass.UNKNOWN:
        Line("My line"),
        # Set your own asset class & subclass:
        Line("Bank account", AssetClass.CASH, AssetSubclass.CCP),
        # 4% expected yearly returns (net of inflation/fees/taxes):
        Line("Real estate", perf=LinePerf(4)),
        Folder(
            "My folder",
            # Set default asset class & subclass for all children:
            asset_class=AssetClass.STOCK,
            asset_subclass=AssetSubclass.ETF,
            perf=LinePerf(8),
            children=[
                # Will inherit asset_class=STOCK, asset_subclass=ETF:
                Line("Line 1"),
                # Override Folder's defaults:
                Line("Line 2", AssetClass.CASH, AssetSubclass.CCP, perf=LinePerf(12)),
                # Subfolders will also inherit:
                Folder("My subfolder", children=[Line("Line 3")]),
            ],
        ),
        # This line will be ignored when computing the global portfolio performance:
        Line("Skipped line", perf=LinePerf(10, skip=True)),
    ],
)


# Run the assistant with the dashboard to see the result graph, then visit the URL:
# > http://127.0.0.1:8000
Assistant(portfolio, launch_dashboard=True, ignore_orphans=True).run()
