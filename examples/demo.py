#!/usr/bin/env python
"""
Finalynx is a tool to organize your investments in a custom hierarchy,
fetch real-time values using the Finary API, set targets, and simulate your
portfolio evolution with optional life events and portfolio operations.

This module is maintained by MadeInPierre.
You can always get the latest version of this module at:
> https://github.com/madeinpierre/finalynx
"""
# noreorder
from rich import inspect, print, pretty, traceback  # noqa
from finalynx import TargetRange, TargetMin, TargetMax, TargetRatio, TargetGlobalRatio  # noqa
from finalynx import Folder, Line, Bucket, SharedFolder, Portfolio, FolderDisplay  # noqa
from finalynx import Copilot, Simulator
from finalynx import Assistant

# Enable rich's features
traceback.install()
pretty.install()

if __name__ in {"__main__", "__mp_main__"}:
    """
    Define groups of Lines, called Buckets, that will be considered as
    a single line in your portfolio.
    """
    bucket_garanti = Bucket(
        "Safe funds",
        [
            Line("Livret A", key="LIVRET A"),
            Line("LDDS", key="Livret de Developpement Durable et Solidaire"),
            Line("Livret Jeune", key="LIVRET JEUNE"),
            Line("Fonds euro", key="Fonds Euro Nouvelle Generation"),
        ],
    )

    """
    Define your complete portfolio structure with Lines, Folders (groups
    of Lines), and SharedFolders (Folder with one Bucket). See the
    README file or the documentation for complete usage instructions.
    """
    portfolio = Portfolio(
        "Portfolio",
        children=[
            Folder(
                "Short Term",
                newline=True,
                children=[
                    Folder(
                        "Daily",
                        target=TargetRange(100, 500, tolerance=100),
                        children=[
                            Line(
                                "Neobank",
                                key="CCP N26",
                            ),
                        ],
                    ),
                    Folder(
                        "Monthly",
                        target=TargetRange(1000, 2000, tolerance=500),
                        children=[
                            Line(
                                "Online Bank",
                                key="CCP Boursorama",
                            ),
                            Line(
                                "Traditional Bank",
                                key="CCP Banque Postale",
                            ),
                        ],
                    ),
                    SharedFolder(
                        "Safety net",
                        bucket=bucket_garanti,
                        target_amount=6000,
                        target=TargetMin(6000),
                    ),
                    SharedFolder(
                        "Projects & Trips",
                        bucket=bucket_garanti,
                        target_amount=2000,
                        target=TargetRange(1500, 2000, tolerance=500),
                    ),
                ],
            ),
            SharedFolder(
                "Medium Term",
                bucket=bucket_garanti,
                target_amount=20000,
                target=TargetMin(20000),
                newline=True,
            ),
            Folder(
                "Long Term (10+ years)",
                children=[
                    SharedFolder(
                        "Guaranteed",
                        bucket=bucket_garanti,
                        target=TargetRatio(25),
                    ),
                    Folder(
                        "Real estate",
                        target=TargetRatio(25),
                        children=[
                            Line("SCPIs, REITs, ..."),
                        ],
                    ),
                    Folder(
                        "Stocks",
                        target=TargetRatio(40),
                        children=[
                            Folder(
                                "ETF World (Business as usual)",
                                target=TargetRatio(60),
                                children=[
                                    Line(
                                        "SP500",
                                        key="Amundi PEA S&P 500 UCITS ETF",
                                        target=TargetRatio(41),
                                    ),
                                    Line(
                                        "Russell 2000",
                                        key="",
                                        target=TargetRatio(9),
                                    ),
                                    Line(
                                        "Europe 600",
                                        key="BNP Paribas Stoxx Europe 600 UCITS ETF Acc",
                                        target=TargetRatio(25),
                                    ),
                                    Line(
                                        "Europe Small Cap",
                                        key="",
                                        target=TargetRatio(5),
                                    ),
                                    Line(
                                        "Emerging markets",
                                        key="Amundi PEA MSCI Emerging Markets UCITS ETF",
                                        target=TargetRatio(14),
                                    ),
                                    Line(
                                        "Japan",
                                        key="",
                                        target=TargetRatio(6),
                                    ),
                                ],
                            ),
                            Folder(
                                "ETF World (ESG)",
                                target=TargetRatio(40),
                                children=[
                                    Line(
                                        "USA ESG",
                                        key="Amundi INDEX MSCI USA SRI UCITS ETF DR",
                                        target=TargetRatio(30),
                                    ),
                                    Line(
                                        "Euro ESG",
                                        key="Amundi EURO ISTOXX CLIMATE PARIS ALIGNED PAB UCITS ETF DR - EUR (C)",
                                        target=TargetRatio(20),
                                    ),
                                    Line(
                                        "Emerging markets ESG",
                                        key="Amundi INDEX MSCI EMERGING MARKETS SRI UCITS ETF DR",
                                        target=TargetRatio(10),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Folder(
                        "Satellite & Fun",
                        target=TargetRatio(10),
                        children=[
                            Line("Dividends, forests, others, ..."),
                        ],
                    ),
                    Line("..."),
                ],
            ),
        ],
    )

    """
    Define your life events and investment strategy on the long term
    to simulate your portfolio's evolution.
    """
    scenario = Simulator()  # TODO Coming soon(ish)!

    """
    Define your monthly investment strategy to get automated investment
    recommendations at each salary day.
    """
    copilot = Copilot()  # TODO Coming soon(ish-ish)!

    # Run all routines and display results in the terminal
    Assistant(
        portfolio,
        ignore_orphans=True,  # Ignore fetched lines that you didn't reference in your portfolio.
        hide_amounts=False,  # Display your portfolio with dots instead of the real values (easier to share).
        hide_root=False,  # Display your portfolio without the root (cosmetic preference).
        show_data=True,  # Show what has been fetched online (e.g. from your Finary account)
    ).run()  # noqa
