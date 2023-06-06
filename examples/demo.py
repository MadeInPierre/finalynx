#!/usr/bin/env python
"""
Welcome to Finalynx!

Finalynx is a tool to organize your investments in a custom hierarchy,
fetch real-time investment values from your personal account using the
Finary API and other pre-built sources, set targets, and simulate your
portfolio evolution with optional life events. Finalynx then outputs a
list of transfers between investments as recommendations to reach your
life goals. Finalynx is available as a CLI tool and as a web dashboard.

Finalynx is not a financial advisor and does not give financial advice.
Use this tool to help you make your own decisions. With that said, have
fun! Contributions and feedback on GitHub are warmly welcome!

This module is maintained by MadeInPierre. You can always get the latest
version of this module at:
> https://github.com/madeinpierre/finalynx

Checkout the documentation and tutorials at:
> https://finalynx.readthedocs.io
"""
# noreorder
from datetime import date
from rich import inspect, print, pretty, traceback  # noqa
from finalynx import TargetRange, TargetMin, TargetMax, TargetRatio, TargetGlobalRatio  # noqa
from finalynx import Folder, Line, Bucket, SharedFolder, Portfolio, FolderDisplay  # noqa
from finalynx import AssetClass, AssetSubclass, Envelope, PEA, AV, PER  # noqa
from finalynx import Copilot, Simulator, Assistant

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
    Define your Envelopes, which are your investment accounts. They can
    be used to store cash, or to store other investments. They can also
    be used to store your debts.
    """
    my_bank = Envelope("Bank", "BAN", date_created=date(2023, 1, 1), key="NAME_IN_FINARY")
    my_av = AV("Linxea Spirit 2", "LIX", date_created=date(2018, 7, 1), key="NAME_IN_FINARY")

    """
    Define your complete portfolio structure with Lines, Folders (groups
    of Lines), and SharedFolders (Folder with one Bucket). See the README
    file or the online documentation for complete usage instructions.
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
                            Line("Neobank", key="CCP N26"),
                        ],
                    ),
                    Folder(
                        "Monthly",
                        target=TargetRange(1000, 2000, tolerance=500),
                        children=[
                            Line("Online Bank", key="CCP Boursorama"),
                            Line("Traditional Bank", key="CCP Banque Postale"),
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

    """
    Run the Assistant to get a complete overview of your portfolio!
    See the available options in the README file or the online documentation.
    """
    assistant = Assistant(
        portfolio,
        buckets=[bucket_garanti],
        envelopes=[my_bank, my_av],
        ignore_orphans=True,  # Ignore fetched lines that you didn't reference in your portfolio.
        hide_amounts=False,  # Display your portfolio with dots instead of the real values (easier to share).
        hide_root=False,  # Display your portfolio without the root (cosmetic preference).
        show_data=True,  # Show what has been fetched online (e.g. from your Finary account)
    )

    """
    Finalynx needs to know where to fetch your data from. You can either
    use the built-in fetchers (see the README file or the online documentation)
    or define your own fetchers.
    """
    # from finalynx.fetch.source_realt import SourceRealT # move this line to the top of the file
    # assistant.add_source(SourceRealT("0xMY_REALT_TOKEN"))

    """
    Run the Assistant to get a complete overview of your portfolio! The run()
    method will fetch your data, compute your portfolio, and display it.
    Optionally, you can use the other methods availavle in the `Assistant` class
    to have more control over the process as run() is just a shortcut.
    """
    assistant.run()

    """
    Optionally, you can launch a web dashboard to get an interactive view!
    """
    # assistant.dashboard()
