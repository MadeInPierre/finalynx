#!/usr/bin/env python
import numpy as np

# Enable rich's features
from rich import print, inspect, pretty, traceback
from rich.columns import Columns
from rich.text import Text
from rich.panel import Panel
traceback.install()
pretty.install()

# Portfolio imports
from finary_assistant import TargetRange, TargetMin, TargetMax, TargetRatio, TargetGlobalRatio
from finary_assistant import Folder, Line, Bucket, SharedFolder, Portfolio

# Fetch imports
from finary_assistant import finary_fetch

# Advisor imports
from finary_assistant import Advisor, Simulator

# Utilities imports
from finary_assistant import console


# Main routine to fetch amounts, process targets and display the tree
def main(portfolio, advisor, scenario):
    # Fill tree with current valuations fetched from Finary
    with console.status('[bold green]Fetching data from Finary...'):
        finary_tree = finary_fetch(portfolio)
    
    # Mandatory step after fetching to process some targets and buckets
    portfolio.process()

    # Get recommendations for immediate investment operations
    advice = advisor.advise(portfolio)

    # Simulate the portolio's evolution through the years by auto-investing each month
    simulation = scenario.simulate(portfolio)

    # Display the entire portfolio and associated recommendations
    console.print('\n', Columns([
        Text(''), 
        Panel(portfolio.build_tree(hide_root=False), title='Portfolio', padding=(1, 4)), 
        Panel(finary_tree, title='Finary data'),
        Panel(advice, title='Advisor'),
        Panel(simulation, title='Simulation'),
    ], padding=(2, 10)))


if __name__ == '__main__':
    '''
    Define groups of Lines, called Buckets, that can be considered as 
    a single line in your portfolio
    '''
    bucket_garanti = Bucket([
        Line('Livret A', key='LIVRET A'),
        Line('LDDS', key='Livret de Developpement Durable et Solidaire'),
        Line('Livret Jeune', key='LIVRET JEUNE'),
        Line('Fonds euro Linxea', key='Fonds Euro Nouvelle Generation'),
    ])

    '''
    Define your complete portfolio structure with Lines, Folders (groups 
    of Lines), and SharedFolders (Folder with one Bucket).
    '''
    portfolio = Portfolio('Patrimoine', children=[
        Folder('Court Terme', newline=True, children=[
            Folder('Quotidien', target=TargetRange(100, 500, tolerance=100), children=[
                Line('N26', key='CCP N26'),
            ]),
            Folder('Mensuel', target=TargetRange(1000, 2000, tolerance=500), children=[
                Line('Boursorama', key='CCP Boursorama'),
                Line('La Banque Postale', key='CCP Banque Postale')
            ]),
            SharedFolder('Précaution', bucket=bucket_garanti, target_amount=6000, target=TargetMin(6000)),
            SharedFolder('Voyages & Projets', bucket=bucket_garanti, target_amount=2000, target=TargetRange(1500, 2000, tolerance=500)),
        ]),
        SharedFolder('Moyen Terme (1-8 ans)', bucket=bucket_garanti, target_amount=20000, target=TargetMin(20000), newline=True),
        Folder('Long Terme (10+ ans)', children=[
            SharedFolder('Tranquille garanti', bucket=bucket_garanti, target=TargetRatio(25)),
            Folder('SCPIs', target=TargetRatio(25), children=[
                Line('Chercher...'),
            ]),
            Folder('Actions', target=TargetRatio(40), children=[
                Folder('ETFs World (Business as usual)', target=TargetRatio(50), children=[
                    Line('SP500', key='Amundi PEA S&P 500 UCITS ETF', target=TargetRatio(41)),
                    Line('Russell 2000', key='', target=TargetRatio(9)),
                    Line('Europe 600', key='BNP Paribas Stoxx Europe 600 UCITS ETF Acc', target=TargetRatio(25)),
                    Line('Europe Small Cap', key='', target=TargetRatio(5)),
                    Line('Emerging markets', key='Amundi PEA MSCI Emerging Markets UCITS ETF', target=TargetRatio(14)),
                    Line('Japon', key='', target=TargetRatio(6))
                ]),
                Folder('ETFs World (Croissance verte)', target=TargetRatio(40), children=[
                    Line('World ESG', key='Amundi MSCI World SRI UCITS ETF DR', target=TargetRatio(50)),
                    Line('USA ESG', key='Amundi INDEX MSCI USA SRI UCITS ETF DR', target=TargetRatio(30)),
                    Line('Euro ESG (PEA)', key='Amundi EURO ISTOXX CLIMATE PARIS ALIGNED PAB UCITS ETF DR - EUR (C)', target=TargetRatio(20)),
                    Line('Euro ESG (AV)', key='Amundi INDEX MSCI EUROPE SRI UCITS ETF DR', target=TargetRatio(0)),
                    Line('Emerging markets ESG', key='Amundi INDEX MSCI EMERGING MARKETS SRI UCITS ETF DR', target=TargetRatio(10)),
                ]),
                Folder('Gestion pilotée ISR', target=TargetRatio(10), children=[
                    Line('Goodvest'),
                ]),
            ]),
            Folder('Satellites & Fun', newline=True, target=TargetRatio(10), children=[
                Line('Crowdfunding'),
                Line('Dividendes, forets, autres, ...'),
            ]),
        ]),
        Folder('Retraite (investissements bloqués)', newline=True, children=[
            Line('Préfon', key='Prefon PER'),
            Line('Linxea Spirit PER'),
        ]),
        Folder('Défense', newline=True, target=TargetRatio(10), children=[
            Line('Or', target=TargetRatio(60)),
            Line('Métaux', target=TargetRatio(20)),
            Line('Cryptos', target=TargetRatio(20)),
        ]),
        Folder('En attente (reventes passifs, liquidités, ...)', children=[
            Line('Moto (à revendre)', key='Moto Z650'),
            Line('Liquidités PEA (à investir)', key='Liquidites'),
            Line('Linxea court terme (à arbitrer)', key='AXA Court Terme AC'),
        ]),
    ])

    '''
    Define your monthly investment strategy to get automated investment 
    recommendations at each salary day.
    '''
    advisor = Advisor()

    '''
    Define your life events and investment strategy on the long term 
    to simulate your portfolio's evolution.
    '''
    scenario = Simulator()

    # Run all routines and display results in the terminal
    main(portfolio, advisor, scenario)