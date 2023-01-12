import numpy as np

# Enable rich's features
from rich import print, inspect, pretty, traceback
from rich.columns import Columns
from rich.panel import Panel
traceback.install()
pretty.install()

from finary_assistant import TargetRange, TargetMin, TargetMax, TargetRatio, TargetGlobalRatio
from finary_assistant import Folder, Line, Bucket, BucketFolder
from finary_assistant import finary_fetch
from finary_assistant import console

if __name__ == '__main__':
    bucket_garanti = Bucket([
        Line("Livret A", key="LIVRET A"),
        Line("LDDS", key="Livret de Developpement Durable et Solidaire"),
        Line("Livret Jeune", key="LIVRET JEUNE"),
        Line("Fonds euro Linxea", key="Fonds Euro Nouvelle Generation"),
    ])

    patrimoine = Folder('Portfolio', children=[
        Folder('Short Term', children=[
            Folder('Daily', target=TargetMax(500, 100), children=[
                Line("CCP N26"),
            ]),
            Folder('Monthly', target=TargetRange(1000, 2000, tolerance=500), children=[
                Line("CCP Boursorama"),
                Line("CCP Banque Postale")
            ]),
            BucketFolder('Safety net', bucket=bucket_garanti, target_amount=6000, target=TargetMin(6000)),
            BucketFolder('Trips & Projects', bucket=bucket_garanti, target_amount=2000, target=TargetRange(1500, 2000, 500)),
        ]),
        BucketFolder('Medium Term (1-8 years)', bucket=bucket_garanti, target_amount=20000, target=TargetMin(20000)),
        Folder('Long Term (10+ years)', children=[
            BucketFolder('Safe zone', bucket=bucket_garanti, target=TargetRatio(25)),
            Folder('SCPIs', target=TargetRatio(15), children=[
                Line('Chercher...'),
            ]),
            Folder('Stocks', target=TargetRatio(50), children=[
                Folder('ETFs World (Business as usual)', target=TargetRatio(50), children=[
                    Line("SP500", key="Amundi PEA S&P 500 UCITS ETF", target=TargetRatio(41)),
                    Line("Russell 2000", key="", target=TargetRatio(9)),
                    Line("Europe 600", key="BNP Paribas Stoxx Europe 600 UCITS ETF Acc", target=TargetRatio(25)),
                    Line("Europe Small Cap", key="", target=TargetRatio(5)),
                    Line("Emerging markets", key="Amundi PEA MSCI Emerging Markets UCITS ETF", target=TargetRatio(14)),
                    Line("Japon", key="", target=TargetRatio(6))
                ]),
                Folder('ETFs World (Croissance verte)', target=TargetRatio(40), children=[
                    Line("World ESG", key="Amundi MSCI World SRI UCITS ETF DR", target=TargetRatio(50)),
                    Line("USA ESG", key="Amundi INDEX MSCI USA SRI UCITS ETF DR", target=TargetRatio(30)),
                    Line("Euro ESG (PEA)", key="Amundi EURO ISTOXX CLIMATE PARIS ALIGNED PAB UCITS ETF DR - EUR (C)", target=TargetRatio(20)),
                    Line("Euro ESG (AV)", key="Amundi INDEX MSCI EUROPE SRI UCITS ETF DR", target=TargetRatio(0)),
                    Line("Emerging markets ESG", key="Amundi INDEX MSCI EMERGING MARKETS SRI UCITS ETF DR", target=TargetRatio(10)),
                ]),
                Folder('Gestion pilotée ISR', target=TargetRatio(10), children=[
                    Line("Goodvest"),
                ]),
            ]),
            Folder('Satellite', target=TargetRatio(10), children=[
                Line('Crowdfunding'),
                Line('Dividendes'),
                Line('Forets'),
                Line('Autres?'),
            ]),
        ]),
        Folder('Retraite', children=[
            Line('Préfon', key='Prefon PER'),
            Line('Linxea Spirit PER'),
        ]),
        Folder('Défense', target=TargetRatio(10), children=[
            Line('Or', target=TargetGlobalRatio(60)),
            Line('Métaux', target=TargetGlobalRatio(20)),
            Line('Cryptos', target=TargetGlobalRatio(20)),
        ]),
        Folder('En attente (reventes passifs, liquidités, ...)', children=[
            Line('Moto', key='Moto Z650'),
            Line('Liquidités PEA', key='Liquidites'),
        ]),
    ])

    # Fill tree with current valuations fetched from Finary
    with console.status("[bold green]Fetching data from Finary...") as status:
        finary_tree = finary_fetch(patrimoine)
    
    # Mandatory step after fetching to process some targets and buckets
    patrimoine.process()

    # Display the final tree and fetched data coming from Finary
    console.print('\n', Columns([patrimoine.build_tree(), Panel(finary_tree, title="Finary data")], padding=(2, 20)))