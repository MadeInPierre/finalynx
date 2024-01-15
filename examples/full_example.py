#!/usr/bin/env python
"""
This file gives you a full example of how to use Finalynx that uses most
of the features offered by Finalynx. Use it as a template to build your own
portfolio.

Finalynx is a tool to organize your investments in a custom hierarchy,
fetch real-time values using the Finary API, set targets, and simulate your
portfolio evolution with optional life events and portfolio operations.

This module is maintained by MadeInPierre.
You can always get the latest version of this module at:
> https://github.com/madeinpierre/finalynx
"""
# noreorder
from datetime import date
from rich import inspect, print, pretty, traceback  # noqa
from finalynx import (
    TargetRange,
    TargetMin,
    TargetMax,
    TargetRatio,
)  # noqa
from finalynx import (
    Sidecar,
    Folder,
    Line,
    LinePerf,
    Bucket,
    SharedFolder,
    Portfolio,
    FolderDisplay,
)  # noqa
from finalynx import Envelope, PEA, PEE, AV, PER
from finalynx import AssetClass, AssetSubclass
from finalynx import Simulation, AddLineAmount, Event, Salary
from finalynx import Assistant

# Enable rich's features
traceback.install()
pretty.install()


if __name__ in {"__main__", "__mp_main__"}:
    """
    (Optional) Custom shortcuts in variables used below to control the config quickly.
    """
    short_display = FolderDisplay.EXPANDED  # Display style for all short-term folders
    medium_term_amount = 20000  # Amount of money to keep for medium-term (i.e. Livrets in this config)
    date_retirement = date(2063, 7, 1)

    # Define envelopes used in the portfolio
    bank_lbp = Envelope("La Banque Postale", "LBP")
    bank_n26 = Envelope("N26", "N26")
    bank_boursorama = Envelope("BoursoBank", "BOU")
    bank_revolut = Envelope("Revolut", "REV")

    pea = PEA("Bourse Direct", "PEA", date(2022, 7, 1), key="MR LACLAU PIERRE (Compte PEA)")
    pee = PEE(
        "Natixis",
        "PEE",
        date(2023, 4, 1),
        date_unlock=date(2023, 11, 22),
        key="Plan d'Epargne Entreprise",
    )

    av_linxea = AV("Linxea Spirit 2", "LIX", date(2022, 7, 1), key="LINXEA Spirit 2")
    av_goodvest = AV("Goodvest", "GOO", date(2022, 7, 1))
    av_ramify = AV("Ramify", "RAM", date(2022, 7, 1), key="Ramify AV")

    per_linxea = PER("Linxea Spirit PER", "PER", date(2022, 7, 1), date_retirement)
    per_prefon = PER("Prefon", "PRF", date(2022, 7, 1), date_retirement, key="Autres actifs")

    cto_tr = Envelope("Trade Republic", "TRP", key="Trade Republic Portfolio")

    at_home = Envelope("At Home", "PHY", key="Metaux precieux")

    """
    (Optional) Declare some of the lines beforehand to save them in a variable. This
    is useful for some of Finalynx's features, such as the portfolio simulation. Here,
    we declare the Livret A line which will receive our future monthly savings.
    """
    livreta = Line(
        "Livret A",
        AssetClass.GUARANTEED,
        AssetSubclass.LIVRET,
        key="LIVRET A",
        envelope=bank_lbp,
        perf=LinePerf(2),
    )

    """
    Define buckets used in the portfolio. Buckets are used to group lines together,
    they will be treated as a single line. The bucket can be used in several locations
    in the portfolio with `SharedFolder`s.

    We add the Livret A line to the bucket so that it will be present in the portfolio.
    """
    bucket_livrets = Bucket(
        "Fonds garantis",
        [
            livreta,
            Line(
                "LDDS",
                AssetClass.GUARANTEED,
                AssetSubclass.LIVRET,
                key="Livret de Developpement Durable et Solidaire",
                envelope=bank_lbp,
                perf=LinePerf(2),
            ),
            Line(
                "Livret Jeune",
                AssetClass.GUARANTEED,
                AssetSubclass.LIVRET,
                key="LIVRET JEUNE",
                envelope=bank_lbp,
                perf=LinePerf(2),
            ),
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
                newline=True,
                display=FolderDisplay.EXPANDED,
                target=TargetRange(5000, 10000),
                children=[
                    Folder(
                        "Quotidien",
                        target=TargetRange(100, 500, tolerance=100),
                        display=short_display,
                        children=[
                            Line(
                                "N26",
                                AssetClass.CASH,
                                AssetSubclass.CCP,
                                key="CCP N26",
                                target=TargetRange(100, 500, tolerance=100),
                                envelope=bank_n26,
                            ),
                            Line(
                                "Revolut",
                                AssetClass.CASH,
                                AssetSubclass.CCP,
                                key="Revolut Current EUR",
                                target=TargetRange(100, 500, tolerance=100),
                                envelope=bank_revolut,
                            ),
                        ],
                    ),
                    Folder(
                        "Mensuel",
                        target=TargetRange(500, 1500, tolerance=500),
                        display=short_display,
                        children=[
                            Line(
                                "La Banque Postale",
                                AssetClass.CASH,
                                AssetSubclass.CCP,
                                key="CCP Banque Postale",
                                envelope=bank_lbp,
                            ),
                        ],
                    ),
                    SharedFolder(
                        "Epargne de précaution",
                        bucket=bucket_livrets,
                        target_amount=5000,
                        target=TargetMin(5000),
                        display=short_display,
                    ),
                    SharedFolder(
                        "Voyages & Projets",
                        bucket=bucket_livrets,
                        target_amount=2000,
                        target=TargetRange(1500, 2000, tolerance=500),
                        newline=True,
                        display=short_display,
                    ),
                ],
            ),
            ######
            ######
            ######
            SharedFolder(
                "Moyen Terme",
                bucket=bucket_livrets,
                target_amount=medium_term_amount,
                target=TargetMin(medium_term_amount),
                display=short_display,
                newline=True,
            ),
            ######
            ######
            ######
            Folder(
                "Long Terme",
                children=[
                    Folder(
                        "Tranquille garanti",
                        target=TargetRatio(20),
                        perf=LinePerf(4.5),
                        newline=True,
                        children=[
                            # Anything above the previous SharedFolders' targets will be appear here.
                            # The target is set to 0% so that the money is automatically invested
                            # in the other lines in the Long Term folder based on their targets.
                            SharedFolder(
                                "Surplus livrets",
                                bucket=bucket_livrets,
                                target=TargetRatio(0),
                                display=FolderDisplay.LINE,
                            ),
                            Line(
                                "Fonds euro",
                                AssetClass.GUARANTEED,
                                AssetSubclass.FOND_EURO,
                                key="304811",
                                target=TargetRatio(100),
                                envelope=av_linxea,
                                perf=LinePerf(3.5),
                                newline=True,
                            ),
                        ],
                    ),
                    Folder(
                        "Immobilier papier",
                        target=TargetRatio(10),
                        perf=LinePerf(4.5),
                        children=[
                            Line(
                                "Remake Live",
                                AssetClass.REAL_ESTATE,
                                AssetSubclass.SCPI,
                                key="104063",
                                target=TargetRatio(25),
                                envelope=av_linxea,
                                perf=LinePerf(5.5),
                            ),
                            Line(
                                "Pierval santé",
                                AssetClass.REAL_ESTATE,
                                AssetSubclass.SCPI,
                                key="",
                                target=TargetRatio(25),
                                envelope=av_linxea,
                            ),
                            Line(
                                "Activimmo",
                                AssetClass.REAL_ESTATE,
                                AssetSubclass.SCPI,
                                key="",
                                target=TargetRatio(25),
                                envelope=av_linxea,
                            ),
                            Line(
                                "Atream Hotels",
                                AssetClass.REAL_ESTATE,
                                AssetSubclass.SCPI,
                                key="",
                                target=TargetRatio(25),
                                newline=True,
                                envelope=av_linxea,
                            ),
                        ],
                    ),
                    Folder(
                        "Actions",
                        asset_class=AssetClass.STOCK,
                        asset_subclass=AssetSubclass.ETF,
                        target=TargetRatio(50),
                        perf=LinePerf(6),
                        children=[
                            Folder(
                                "USA",
                                target=TargetRatio(50),
                                children=[
                                    Line(
                                        "SP500 [italic](PE500)[/]",
                                        key="13577960",
                                        target=TargetRatio(50),
                                        envelope=pea,
                                    ),
                                    Line(
                                        "SP500 ESG [italic](xxxxx)[/]",
                                        key="13578020",
                                        target=TargetRatio(30),
                                        envelope=av_linxea,
                                    ),
                                    Line(
                                        "Russell 2000 [italic](RS2K)[/]",
                                        key="13577964",
                                        target=TargetRatio(20),
                                        envelope=pea,
                                    ),
                                ],
                            ),
                            Folder(
                                "Europe",
                                target=TargetRatio(30),
                                children=[
                                    Line(
                                        "Europe 600 ESG [italic](PABZ)[/]",
                                        key="13577963",
                                        target=TargetRatio(80),
                                        envelope=pea,
                                    ),
                                    Line(
                                        " Europe 600 [italic](ETZ)[/]",
                                        key="13577961",
                                        target=TargetRatio(20),
                                        envelope=pea,
                                    ),
                                ],
                            ),
                            Folder(
                                "Reste du monde",
                                target=TargetRatio(20),
                                children=[
                                    Line(
                                        "Emerging markets [italic](PAEEM)[/]",
                                        key="13577962",
                                        target=TargetRatio(50),
                                        envelope=pea,
                                    ),
                                    Line(
                                        "Emerging markets ESG [italic](xxxxx)[/]",
                                        key="8804145",
                                        target=TargetRatio(30),
                                        envelope=av_linxea,
                                    ),
                                    Line(
                                        "Japon [italic](PTPXE)[/]",
                                        key="",
                                        target=TargetRatio(20),
                                        newline=True,
                                        envelope=pea,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Folder(
                        "Gestion pilotée",
                        target=TargetRatio(10),
                        perf=LinePerf(5),
                        children=[
                            # Fetched lines from these accounts will be automatically added to these folders
                            Folder(
                                "Ramify",
                                asset_class=AssetClass.STOCK,
                                asset_subclass=AssetSubclass.DIVERSIFIED,
                                target=TargetRatio(50),
                                display=FolderDisplay.LINE,
                                envelope=av_ramify,
                            ),
                            Folder(
                                "Goodvest",
                                asset_class=AssetClass.STOCK,
                                asset_subclass=AssetSubclass.DIVERSIFIED,
                                target=TargetRatio(50),
                                display=FolderDisplay.LINE,
                                newline=True,
                                envelope=av_goodvest,
                            ),
                        ],
                    ),
                    Folder(
                        "Défense",
                        target=TargetRatio(10, zone=2),
                        children=[
                            Folder(
                                "Or",
                                display=FolderDisplay.LINE,
                                target=TargetRatio(60, zone=2),
                                perf=LinePerf(2),
                                children=[
                                    Line(
                                        "2x 20 Francs Marianne Coq",
                                        AssetClass.MATERIAL,
                                        AssetSubclass.GOLD,
                                        envelope=at_home,
                                        key="21864",
                                    ),
                                    Line(
                                        "4x 20 Francs Marianne Coq",
                                        AssetClass.MATERIAL,
                                        AssetSubclass.GOLD,
                                        # envelope=at_home,
                                        key="27669",
                                    ),
                                ],
                            ),
                            Folder(
                                "Cryptos",
                                display=FolderDisplay.LINE,
                                target=TargetRatio(40, zone=2),
                                perf=LinePerf(0),
                                newline=True,
                                children=[
                                    Line(
                                        "Bitcoin",
                                        AssetClass.CRYPTO,
                                        AssetSubclass.L1,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            Folder(
                "Bloqué",
                perf=LinePerf(0, skip=True),
                children=[
                    Line(
                        "PEE (à récupérer)",
                        AssetClass.CASH,
                        AssetSubclass.MONETARY,
                        key="13009544",
                        envelope=pee,
                    ),
                    Line(
                        "Shares To Win Stellantis (à récupérer)",
                        AssetClass.STOCK,
                        AssetSubclass.STOCK_SHARE,
                        key="13417344",
                        envelope=pee,
                        newline=True,
                    ),
                ],
            ),
            Folder(
                "Retraite",
                perf=LinePerf(0, skip=True),
                children=[
                    Line(
                        "Remake Live",
                        AssetClass.REAL_ESTATE,
                        AssetSubclass.SCPI,
                        key="106040",
                        envelope=per_linxea,
                        perf=LinePerf(5.5),
                    ),
                    Line(
                        "Fonds Euro PER",
                        AssetClass.GUARANTEED,
                        AssetSubclass.FOND_EURO,
                        key="319493",
                        envelope=per_linxea,
                        perf=LinePerf(3.5),
                    ),
                    Line(
                        "Prefon PER",
                        AssetClass.GUARANTEED,
                        AssetSubclass.FOND_EURO,
                        key="22276",
                        newline=True,
                        envelope=per_prefon,
                    ),
                ],
            ),
            Folder(
                "En attente",
                perf=LinePerf(0, skip=True),
                children=[
                    Line(
                        "Boursorama (à remplacer)",
                        AssetClass.CASH,
                        AssetSubclass.CCP,
                        key="CCP Boursorama",
                        envelope=bank_boursorama,
                    ),
                    Line(
                        "Liquidités PEA (à investir)",
                        AssetClass.CASH,
                        AssetSubclass.LIQUIDITY,
                        key="13577959",
                        envelope=pea,
                        target=TargetMax(0),
                    ),
                    Line(
                        "AXA Court Terme (à arbitrer)",
                        AssetClass.CASH,
                        AssetSubclass.MONETARY,
                        key="10035637",
                        envelope=av_linxea,
                        target=TargetMax(0),
                    ),
                    Line(
                        "Europe 600 ESG sur AV",
                        AssetClass.STOCK,
                        AssetSubclass.ETF,
                        key="8804144",
                        envelope=av_linxea,
                        target=TargetMax(0),
                    ),
                    Line(
                        "World ESG sur AV",
                        AssetClass.STOCK,
                        AssetSubclass.ETF,
                        key="8804143",
                        envelope=av_linxea,
                        target=TargetMax(0),
                    ),
                    Line(
                        "Livret Trade Republic",
                        AssetClass.GUARANTEED,
                        AssetSubclass.LIVRET_TAXED,
                        key="13666160",
                        envelope=cto_tr,
                        newline=True,
                    ),
                ],
            ),
        ],
    )

    """
    Run all routines and display results in the terminal.
    See the documentation for more details on the parameter options.
    """
    assistant = Assistant(
        portfolio,
        buckets=[
            bucket_livrets,
        ],
        envelopes=[
            bank_lbp,
            bank_n26,
            bank_boursorama,
            pea,
            pee,
            av_linxea,
            av_goodvest,
            av_ramify,
            per_linxea,
            per_prefon,
            at_home,
        ],
        ignore_orphans=False,
        hide_amounts=False,
        hide_root=False,
        show_data=False,
        check_budget=False,
        sidecars=[
            Sidecar("[ideal]", "[delta]", render_folders=False),
            Sidecar("[delta]", render_folders=False),
            Sidecar("[perf]", render_folders=False),
        ],
        simulation=Simulation(
            events=[
                Salary(livreta, income=2300, expenses=1400, end_date=date(2024, 11, 30)),
                Event(
                    AddLineAmount(livreta, 3500),
                    planned_date=date(2024, 4, 10),
                    name="Prime",
                ),
                Event(
                    AddLineAmount(livreta, 3500),
                    planned_date=date(2025, 4, 10),
                    name="Prime",
                ),
                Salary(
                    livreta,
                    income=3500,
                    expenses=2000,
                    start_date=date(2025, 1, 1),
                    income_growth=1,  # 1% income gain per year (net of inflation)
                    expenses_follow=75,  # 75% of the gains are used to increase expenses, 25% saved
                    name="Futur Job",
                ),
            ],
            inflation=3.0,
            end_date=date(1998 + 65, 4, 5),
            step_years=5,
        ),
    )

    """
    Run the assistant! The `run` method does the most common operations. Optionally,
    you can call the other methods in the `Assistant` class individually.
    """
    assistant.run()

    """
    (Optional) Export the portfolio to an image before quitting.
    Useful when this is called by the Telegram bot.
    """
    # assistant.export_img(size=(1930, 3200))
