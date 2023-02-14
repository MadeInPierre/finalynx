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
def main(portfolio, scenario, advisor, ignore_orphans=False, hide_amount=False):
    # Fill tree with current valuations fetched from Finary
    with console.status('[bold green]Fetching data from Finary...'):
        finary_tree = finary_fetch(portfolio, ignore_orphans)
    
    # Mandatory step after fetching to process some targets and buckets
    portfolio.process()

    # Simulate the portolio's evolution through the years by auto-investing each month
    simulation = scenario.simulate(portfolio)

    # Get recommendations for immediate investment operations
    advice = advisor.advise(portfolio)

    # Display the entire portfolio and associated recommendations
    console.print('\n', Columns([
        Panel(portfolio.rich_tree(hide_amount=hide_amount, hide_root=False), title='Portfolio', padding=(1, 4)), 
        Panel(finary_tree, title='Finary data'),
        # Panel(simulation, title='Simulation'), # TODO Coming soon
        # Panel(advice, title='Advisor'),        # TODO Coming soon
    ], padding=(2, 10)))


if __name__ == '__main__':
    '''
    Define groups of Lines, called Buckets, that will be considered as 
    a single line in your portfolio
    '''
    bucket_garanti = Bucket([
        Line('Livret A', key='LIVRET A'),
        Line('LDDS', key='Livret de Developpement Durable et Solidaire'),
        Line('Livret Jeune', key='LIVRET JEUNE'),
        Line('Fonds euro', key='Fonds Euro Nouvelle Generation'),
    ])

    '''
    Define your complete portfolio structure with Lines, Folders (groups 
    of Lines), and SharedFolders (Folder with one Bucket). See the 
    README file or the documentation for complete usage instructions.
    '''
    portfolio = Portfolio('Portfolio', children=[
        Folder('Short Term', newline=True, children=[
            Folder('Daily', target=TargetRange(100, 500, tolerance=100), children=[
                Line('Neobank', key='CCP N26'),
            ]),
            Folder('Monthly', target=TargetRange(1000, 2000, tolerance=500), children=[
                Line('Online Bank', key='CCP Boursorama'),
                Line('Traditional Bank', key='CCP Banque Postale')
            ]),
            SharedFolder('Safety net', bucket=bucket_garanti, target_amount=6000, target=TargetMin(6000)),
            SharedFolder('Projects & Trips', bucket=bucket_garanti, target_amount=2000, target=TargetRange(1500, 2000, tolerance=500)),
        ]),
        SharedFolder('Medium Term', bucket=bucket_garanti, target_amount=20000, target=TargetMin(20000), newline=True),
        Folder('Long Term (10+ years)', children=[
            SharedFolder('Guaranteed', bucket=bucket_garanti, target=TargetRatio(25)),
            Folder('Real estate', target=TargetRatio(25), children=[
                Line('SCPIs, REITs, ...'),
            ]),
            Folder('Stocks', target=TargetRatio(40), children=[
                Folder('ETF World (Business as usual)', target=TargetRatio(60), children=[
                    Line('SP500', key='Amundi PEA S&P 500 UCITS ETF', target=TargetRatio(41)),
                    Line('Russell 2000', key='', target=TargetRatio(9)),
                    Line('Europe 600', key='BNP Paribas Stoxx Europe 600 UCITS ETF Acc', target=TargetRatio(25)),
                    Line('Europe Small Cap', key='', target=TargetRatio(5)),
                    Line('Emerging markets', key='Amundi PEA MSCI Emerging Markets UCITS ETF', target=TargetRatio(14)),
                    Line('Japan', key='', target=TargetRatio(6))
                ]),
                Folder('ETF World (ESG)', target=TargetRatio(40), children=[
                    Line('USA ESG', key='Amundi INDEX MSCI USA SRI UCITS ETF DR', target=TargetRatio(30)),
                    Line('Euro ESG', key='Amundi EURO ISTOXX CLIMATE PARIS ALIGNED PAB UCITS ETF DR - EUR (C)', target=TargetRatio(20)),
                    Line('Emerging markets ESG', key='Amundi INDEX MSCI EMERGING MARKETS SRI UCITS ETF DR', target=TargetRatio(10)),
                ]),
            ]),
            Folder('Satellite & Fun', target=TargetRatio(10), children=[
                Line('Dividends, forests, others, ...'),
            ]),
            Line('...'),
        ]),
    ])

    '''
    Define your life events and investment strategy on the long term 
    to simulate your portfolio's evolution.
    '''
    scenario = Simulator() # TODO Coming soon(ish)!

    '''
    Define your monthly investment strategy to get automated investment 
    recommendations at each salary day.
    '''
    advisor = Advisor() # TODO Coming soon(ish-ish)!

    # Run all routines and display results in the terminal
    main(portfolio, scenario, advisor, ignore_orphans=True, hide_amount=True)