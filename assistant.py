import numpy as np

# Enable rich's features
from rich import print, inspect, pretty, traceback
from rich.columns import Columns
from rich.panel import Panel
traceback.install()
pretty.install()

from finary_assistant import TargetRange, TargetMin, TargetMax, TargetRatio, TargetGlobalRatio
from finary_assistant import Folder, Line
from finary_assistant import match_finary
from finary_assistant import console

if __name__ == '__main__':
    patrimoine = Folder('Portfolio', children=[
        Folder('Short Term', children=[
            Folder('Daily', children=[
                Line("CCP N26", target=TargetMax(500, 100)),
            ]),
            Folder('Monthly', children=[
                Line("CCP Boursorama", target=TargetMax(1000, 1000)),
                Line("CCP Banque Postale", target=TargetRange(1000, 2000, tolerance=500))
            ]),
            Folder('Safety net', children=[
                Line("LDDS", key="Livret de Developpement Durable et Solidaire", target=TargetMin(6000)),
            ]),
            Folder('Projects & Trips', children=[
                Line("LDDS", key="Livret de Developpement Durable et Solidaire", target=TargetMin(2000)),
            ]),
        ]),
        Folder('Medium Term (1-8 years)', children=[
            Line("Livret A", key="LIVRET A", target=TargetMin(20000)),
            Line("Livret Jeune", key="LIVRET JEUNE", target=TargetMin(1600)),
            Line("Fonds euro Linxea", key="Fonds Euro Nouvelle Generation", target=TargetMin(0)),
        ]),
        Folder('Long Term (10+ years)', children=[
            Folder('Safe', children=[
                Line("Fonds euro Linxea", key="Fonds Euro Nouvelle Generation"),
            ]),
            Folder('SCPIs', children=[
                Line('SCPI 1'),
                Line('SCPI 2'),
                Line('SCPI 3'),
            ]),
            Folder('Stocks', children=[
                Folder('ETF World (Business as usual)', children=[
                    Line("SP500", key="Amundi PEA S&P 500 UCITS ETF", target=TargetRatio(41, 10)),
                    Line("Russell 2000", key="", target=TargetRatio(9, 4)),
                    Line("Europe 600", key="BNP Paribas Stoxx Europe 600 UCITS ETF Acc", target=TargetRatio(25, 10)),
                    Line("Europe Small Cap", key="", target=TargetRatio(5, 4)),
                    Line("Emerging markets", key="Amundi PEA MSCI Emerging Markets UCITS ETF", target=TargetRatio(14, 10)),
                    Line("Japon", key="", target=TargetRatio(6, 4))
                ]),
                Folder('ETF World (Croissance verte)', children=[
                    Line("World ESG", key="Amundi MSCI World SRI UCITS ETF DR", target=TargetRatio(50, 10)),
                    Line("USA ESG", key="Amundi INDEX MSCI USA SRI UCITS ETF DR", target=TargetRatio(30, 10)),
                    Line("Euro ESG (PEA)", key="Amundi EURO ISTOXX CLIMATE PARIS ALIGNED PAB UCITS ETF DR - EUR (C)", target=TargetRatio(20, 10)),
                    Line("Euro ESG (AV)", key="Amundi INDEX MSCI EUROPE SRI UCITS ETF DR", target=TargetRatio(0)),
                    Line("Emerging markets ESG", key="Amundi INDEX MSCI EMERGING MARKETS SRI UCITS ETF DR", target=TargetRatio(10, 10)),
                ]),
                Line("Goodvest"),
            ]),
            Folder('Satellite', children=[
                Line('Crowdfunding'),
                Line('Dividendes'),
                Line('Forets'),
                Line('Autres?'),
            ]),
        ]),
        Folder('Retraite', children=[
            Line('Prefon PER'),
        ]),
        Folder('Défense', children=[
            Line('Or', target=TargetGlobalRatio(6, 2)),
            Line('Argent', target=TargetGlobalRatio(2, 1)),
            Line('Cryptos', target=TargetGlobalRatio(2, 1)),
        ]),
        Folder('En attente (reventes passifs, liquidités, ...)', children=[
            Line('Moto', key='Moto Z650'),
            Line('Liquidités PEA', key='Liquidites'),
        ]),
    ])

    # Fill tree with current valuations fetched from Finary
    with console.status("[bold green]Fetching data from Finary...") as status:
        finary_tree = match_finary(patrimoine)

    console.print(Columns([patrimoine.build_tree(), Panel(finary_tree, title="Finary data")], padding=(2, 50)))