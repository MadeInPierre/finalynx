"""
Finalynx - Tutorial 3.1 - Common template for simulations
==========================================================


This tutorial shows how to organize your portfolio to be compatible with simulations.
There may be various compatible structure, but this one is probably useful for most
people.



See the online documentation for the list of available pre-defined envelopes:
> https://github.com/MadeInPierre/finalynx/blob/main/finalynx/portfolio/envelopes.py

Try it out by running:
> python3 examples/tutorials/3_simulation/1_basics.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio, Line, SharedFolder, Folder, Bucket
from finalynx import Simulation, Event, Salary, AddLineAmount, date
from finalynx import TargetRange, TargetMin, TargetRatio, LinePerf

"""
(Optional) Declare some of the lines beforehand to save them in a variable. This
is useful for some of Finalynx's features, such as the portfolio simulation. Here,
we declare the Livret A line which will receive our future monthly savings.
"""
livreta = Line("Livret A", perf=LinePerf(3))

"""
Define buckets used in the portfolio. Buckets are used to group lines together,
they will be treated as a single line. The bucket can be used in several locations
in the portfolio with `SharedFolder`s.

We add the Livret A line to the bucket so that it will be present in the portfolio.
"""
bucket_livrets = Bucket(
    "Fonds garantis",
    lines=[
        livreta,
        Line("LDDS", perf=LinePerf(3)),
    ],
)

"""
Define the full portfolio hierarchy. The portfolio is a tree of folders and lines.

The previous bucket is used in the Short and Medium term folders (wich specified
amounts) as well as Long term (with target set at 0%, meaning anything above the
previous targets will be automatically invested in the other long term lines in
the portfolio).
"""
portfolio = Portfolio(
    "Portefeuille",
    children=[
        Folder(
            "Court Terme",
            target=TargetRange(5000, 10000),
            children=[
                Line("Bank N26", target=TargetRange(500, 1500)),
                SharedFolder(
                    "Epargne de précaution",
                    bucket=bucket_livrets,
                    target_amount=5000,
                    target=TargetMin(5000),
                ),
            ],
        ),
        ######
        SharedFolder(
            "Moyen Terme",
            bucket=bucket_livrets,
            target_amount=20000,
            target=TargetMin(20000),
        ),
        ######
        Folder(
            "Long Terme",
            children=[
                Folder(
                    "Tranquille garanti",
                    target=TargetRatio(20),
                    children=[
                        # Anything above the previous SharedFolders' targets will be appear here.
                        # The target is set to 0% so that the money is automatically invested
                        # in the other lines in the Long Term folder based on their targets.
                        #
                        # NOTE: ONLY USE TargetRatio TARGETS IN THE LONG TERM FOLDER
                        # WHEN USING THE SIMULATION ENGINE
                        SharedFolder("Surplus livrets", bucket=bucket_livrets, target=TargetRatio(0)),
                        Line("Fonds euro", target=TargetRatio(100), perf=LinePerf(3)),
                    ],
                ),
                Folder(
                    "Immobilier papier",
                    target=TargetRatio(30),
                    perf=LinePerf(4.5),  # Applied to all children (if not overridden)
                    children=[
                        Line("Remake Live", target=TargetRatio(34), perf=LinePerf(5.5)),
                        Line("Pierval santé", target=TargetRatio(33)),
                        Line("Activimmo", target=TargetRatio(33)),
                    ],
                ),
                Folder(
                    "Actions",
                    target=TargetRatio(50),
                    perf=LinePerf(8),
                    children=[
                        Line("ETF SP500", target=TargetRatio(50)),
                        Line("ETF Europe 600", target=TargetRatio(30)),
                        Line("ETF Emerging Markets", target=TargetRatio(20)),
                    ],
                ),
            ],
        ),
    ],
)


Assistant(
    portfolio,
    buckets=[bucket_livrets],
    envelopes=[],
    # ... other options,
    simulation=Simulation(
        events=[
            Salary(livreta, income=2300, expenses=1400, end_date=date(2024, 11, 30)),
            Event(AddLineAmount(livreta, 3500), planned_date=date(2024, 4, 10), name="Prime"),
            Event(AddLineAmount(livreta, 3500), planned_date=date(2025, 4, 10), name="Prime"),
            Salary(livreta, income=3000, expenses=2000, start_date=date(2025, 1, 1), name="Futur Job"),
        ],
        inflation=3.0,
        end_date=date(2063, 4, 5),
    ),
).run()


""" [COMMAND LINE] ------------------------------------------------------------
You can see the final portfolio amounts at the end of the simulation by running:
"""
# > python your_config.py --future
