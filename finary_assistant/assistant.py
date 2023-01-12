import finary_api.__main__ as ff
from unidecode import unidecode
from enum import Enum
import numpy as np
import json

# Enable rich's features
from rich import print, inspect, pretty, traceback
from rich.console import Console
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.tree import Tree
from rich.text import Text
traceback.install()
pretty.install()

console = Console()

'''--------------------------------------------------------------------------------------------------------------
########################################### FINARY REQUEST & PARSING ############################################
--------------------------------------------------------------------------------------------------------------'''

def match_finary(patrimoine):
    def match_line(patrimoine, key, amount, node, indent=0):
        key, amount = unidecode(key), round(amount)
        node_child = node.add(f"{amount} {key}")
        if not patrimoine.set_child_amount(key, amount):
            node_child.add('[yellow]WARNING: This line did not match with any envelope, attaching to root')
            patrimoine.add_child(Line(key, amount=amount))

    tree = Tree("Finary API", highlight=True, hide_root=True)

    # Login to Finary
    console.log('Signing in to Finary using credentials in \'credentials.json\'...')
    result = ff.signin()
    if result is None or result['message'] != 'Created':
        return tree
    console.log('Successfully signed in')
    session = ff.prepare_session()

    # Comptes courants, Livrets et Fonds euro
    checkings = ff.get_checking_accounts(session, '1w')['result']
    savings = ff.get_savings_accounts(session, '1w')['result']
    fonds = ff.get_fonds_euro(session, '1w')['result']
    for result, name in zip([checkings, savings, fonds], ['Comptes courants', 'Livrets', 'Fonds euro']):
        console.log(f'Fetching {name.lower()}...')
        node = tree.add('[bold]' + str(round(result['timeseries'][-1][1])) + ' ' + name)
        for k, e in result['distribution'].items():
            match_line(patrimoine, k, e['amount'], node, indent=1)

    # Autres
    console.log(f'Fetching other assets...')
    other = ff.get_other_assets(session, '1w')['result']
    f_other_total = round(other['timeseries'][-1][1])
    node = tree.add('[bold]' + str(round(f_other_total)) + ' Autres')
    for item in other['data']:
        match_line(patrimoine, item['name'], item['current_value'], node, indent=1)

    # Investissements
    console.log(f'Fetching investments...')
    investments = ff.get_portfolio_investments(session)['result']
    f_invest_total = round(investments['total']['amount'])
    node = tree.add('[bold]' + str(round(f_invest_total)) + ' Investissements')
    for account in investments['accounts']:
        node_account = node.add("[bold]Account: " + account['name'])
        for category in ['fiats', 'securities', 'cryptos', 'fonds_euro', 'startups', 'precious_metals', 'scpis', 'generic_assets', 'real_estates', 'loans', 'crowdlendings']:
            for item in account[category]:
                match_line(patrimoine, item['security']['name'], item['current_value'], node_account, indent=2)
    
    return tree


'''--------------------------------------------------------------------------------------------------------------
############################################ PORTFOLIO TREE OBJECTS #############################################
--------------------------------------------------------------------------------------------------------------'''


class Hierarchy:
    def __init__(self, parent = None):
        self.parent = parent
    
    def set_parent(self, parent):
        self.parent = parent


class Node(Hierarchy):
    def __init__(self, name, parent=None, target=None):
        super().__init__(parent)
        self.name = name
        self.target = target if target is not None else Target()
        self.target.set_parent(self)

        if target is not None:
            target.set_parent(self)
    
    def get_amount(self):
        raise NotImplementedError("Must be implemented by children classes")
    
    def build_tree(self, tree=None, **args):
        if tree is None:
            return Tree(str(self), **args)
        return tree.add(str(self))
    
    def _render_amount(self):
        max_length = np.max([len(str(round(c.get_amount()))) for c in self.parent.children]) if (self.parent and self.parent.children) else 0
        return self.target.render_amount(n_characters=max_length)
    
    def _render_name(self):
        return self.name
    
    def __str__(self):
        hint = f'[dim white] - {self.target.hint()}[/]' if self.target.check() not in [Target.RESULT_NONE, Target.RESULT_START] else ''
        return f'{self._render_amount()} {self._render_name()}' + hint


class Line(Node):
    def __init__(self, name, parent=None, target=None, key=None, amount=0):
        super().__init__(name, parent, target)
        self.key = key if key is not None else name
        self.amount = amount
    
    def get_amount(self):
        return self.amount


class Folder(Node):
    def __init__(self, name, parent=None, target=None, children=None):
        super().__init__(name, parent, target)
        self.children = [] if children is None else children

        for child in self.children:
            child.set_parent(self)
    
    def add_child(self, child):
        child.set_parent(self)
        self.children.append(child)
    
    def get_amount(self):
        return np.sum([child.get_amount() for child in self.children]) if self.children else 0

    def build_tree(self, tree=None, **args):
        node = Tree(str(self), guide_style='blue', **args) if tree is None else tree.add(str(self))
        for child in self.children:
            child.build_tree(node)
        return node
    
    def set_child_amount(self, key, amount):
        for child in self.children:
            if isinstance(child, Line) and child.key == key:
                child.amount = amount
                return True
            elif isinstance(child, Folder) and child.set_child_amount(key, amount) == True:
                 return True
        return False
    
    def _render_name(self):
        return f'[blue bold]{self.name}[/]'


'''--------------------------------------------------------------------------------------------------------------
############################################## INVESTMENT TARGETS ###############################################
--------------------------------------------------------------------------------------------------------------'''


class Target(Hierarchy):
    RESULT_NOK       = {'name': 'Not OK',    'symbol': '×', 'color': 'red'    }
    RESULT_OK        = {'name': 'OK',        'symbol': '✓', 'color': 'green'  }
    RESULT_TOLERATED = {'name': 'Tolerated', 'symbol': '≈', 'color': 'yellow' }
    RESULT_INVEST    = {'name': 'Invest',    'symbol': '↗', 'color': 'red'    }
    RESULT_DEVEST    = {'name': 'Devest',    'symbol': '↘', 'color': 'red'    }
    RESULT_START     = {'name': 'Start',     'symbol': '↯', 'color': 'cyan'   }
    RESULT_NONE      = {'name': 'No target', 'symbol': '‣', 'color': 'magenta'}

    def __init__(self, parent=None):
        super().__init__(parent)
    
    def get_amount(self):
        if self.parent is None:
            raise ValueError('[red]Target has no parent, not allowed.[/]')
        return self.parent.get_amount()
    
    def check(self):
        if self.get_amount() == 0:
            return Target.RESULT_START
        return Target.RESULT_NONE
    
    def hint(self):
        return 'Gotta invest!' if self.check() == Target.RESULT_START else 'No target'
    
    def render_amount(self, n_characters=0):
        result = self.check() 
        result = result if result != True else Target.RESULT_NOK # TODO weird bug??? Workaround for now
        return f'[{result["color"]}]{result["symbol"]} {round(self.get_amount()):>{n_characters}} €[/]'
    

class TargetRange(Target):
    def __init__(self, target_min, target_max, tolerance=0, parent=None):
        super().__init__(parent)
        self.target_min = target_min
        self.target_max = target_max
        self.tolerance = tolerance
    
    def check(self):
        if super_result := super().check() != Target.RESULT_NONE:
            return super_result
        elif self._get_variable() < self.target_min - self.tolerance:
            return Target.RESULT_INVEST
        elif self._get_variable() < self.target_min:
            return Target.RESULT_TOLERATED
        elif self._get_variable() < self.target_max:
            return Target.RESULT_OK
        elif self._get_variable() < self.target_max + self.tolerance:
            return Target.RESULT_TOLERATED
        return Target.RESULT_DEVEST
    
    def _get_variable(self):
        return self.get_amount()
    
    def hint(self):
        return f'Objective {self.target_min}-{self.target_max} €'


class TargetMax(TargetRange):
    def __init__(self, target_max, tolerance=0, parent=None):
        super().__init__(0, target_max, tolerance, parent)
    
    def hint(self):
        return f'Maximum {self.target_max} €'


class TargetMin(TargetRange):
    def __init__(self, target_min, tolerance=0, parent=None):
        super().__init__(target_min, np.inf, tolerance, parent)
    
    def hint(self):
        return f'Minimum {self.target_min} €'


class TargetRatio(TargetRange):
    def __init__(self, target_ratio, zone=0, tolerance=0, parent=None): # TODO rename zone?
        target_min = max(target_ratio - zone, 0)
        target_max = min(target_ratio + zone, 100)
        super().__init__(target_min, target_max, tolerance, parent)
        self.target_ratio = target_ratio
    
    def get_ratio(self):
        total = self._get_reference_amount()
        return 100 * self.get_amount() / total if total > 0 else 0
    
    def _get_variable(self):
        return self.get_ratio()
    
    def _get_reference_amount(self):
        return self.parent.parent.get_amount()
    
    def hint(self):
        return f'Ratio {round(self.get_ratio())}% → {self.target_ratio}%'


class TargetGlobalRatio(TargetRatio):
    def __init__(self, target_ratio, tolerance=0, parent=None):
        super().__init__(target_ratio, tolerance, parent)
    
    def _get_reference_amount(self):
        root = self.parent
        while root.parent is not None:
            root = root.parent
        return root.get_amount()
    
    def hint(self):
        return f'Global ratio {round(self.get_ratio())}% → {self.target_ratio}%'


'''--------------------------------------------------------------------------------------------------------------
###################################### ENTRY POINT & PORTFOLIO DEFINITION #######################################
--------------------------------------------------------------------------------------------------------------'''


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