import finary_api.__main__ as ff
from unidecode import unidecode
from termcolor import colored
from enum import Enum
import numpy as np
import json

def pprint(s):
    print(json.dumps(s, indent=4))

def match_finary(session, patrimoine):
    def match_line(patrimoine, key, amount, indent=0):
        key, amount = unidecode(key), float(amount)
        print(' ' * indent * 4 + f"{colored(amount, 'white')} {key}")
        if not patrimoine.set_line_amount(key, amount):
            print(colored(' ' * (indent * 4 + 4) + 'WARNING: This line did not match with any envelope, attaching to root', 'yellow'))
            patrimoine.add_line(Line(key, None, None, amount=amount))

    # Comptes courants, Livrets et Fonds euro
    checkings = ff.get_checking_accounts(session, '1w')['result']
    savings = ff.get_savings_accounts(session, '1w')['result']
    fonds = ff.get_fonds_euro(session, '1w')['result']
    for result, name in zip([checkings, savings, fonds], ['Comptes courants', 'Livrets', 'Fonds euro']):
        print(colored(int(result['timeseries'][-1][1]), 'white') + ' ' + name)
        for k, e in result['distribution'].items():
            match_line(patrimoine, k, e['amount'], indent=1)

    # Autres
    other = ff.get_other_assets(session, '1w')['result']
    f_other_total = float(other['timeseries'][-1][1])
    print(colored(round(f_other_total), 'white') + ' Autres')
    for item in other['data']:
        match_line(patrimoine, item['name'], item['current_value'], indent=1)

    # Investissements
    investments = ff.get_portfolio_investments(session)['result']
    f_invest_total = float(investments['total']['amount'])
    print(colored(round(f_invest_total), 'white') + ' Investissements')
    for account in investments['accounts']:
        print("    Account:", account['name'])
        for category in ['fiats', 'securities', 'cryptos', 'fonds_euro', 'startups', 'precious_metals', 'scpis', 'generic_assets', 'real_estates', 'loans', 'crowdlendings']:
            for item in account[category]:
                match_line(patrimoine, item['security']['name'], item['current_value'], indent=2)


class AssetType(Enum):
    CCP          = 'CCP'
    LIVRET       = 'Livret'
    FOND_EURO    = 'Fonds euro'
    ETF          = 'ETF'
    STOCK        = 'Action'
    OBLIGATION   = 'Obligation'
    CROWDFUNDING = 'Crowdfunding'
    GOLD         = 'Or'
    SILVER       = 'Argent'
    PILOTED       = 'Gestion pilotee'
    CRYPTO       = 'Cryptos'
    FOREST       = 'Forets'
    SCPI         = 'SCPI'
    HOUSING      = 'Immobilier'
    PASSIVE      = 'Passif'


class EnvelopeType(Enum):
    CCP      = 'CCP'
    LIVRET   = 'Livret'
    AV       = 'AV'
    PEA      = 'PEA'
    CTO      = 'CTO'
    PER      = 'PER'
    WALLET   = 'Wallet'
    PLATFORM = 'Plateforme'
    PHYSICAL = 'Physique'
    PASSIVE  = 'Passif'


class Line:
    def __init__(self, name, asset_type, envelope_type, parent=None, target=None, amount=0, key=None):
        self.name = name
        self.key = name if key is None else key
        self.asset_type = asset_type
        self.envelope_type = envelope_type
        self.parent = parent
        self.amount = amount
        self.target = target

        if self.target is not None:
            self.target.set_parent(self)
    
    def set_amount(self, amount):
        self.amount = float(amount)
    
    def get_amount(self):
        return self.amount
    
    def set_parent(self, parent):
        self.parent = parent
    
    def get_amount_length(self):
        return len(str(int(self.amount)))
    
    def get_text(self, amount_length=None):
        amount_length = self.get_amount_length() if amount_length is None else amount_length
        check_result = self.target.check() if self.target is not None else None
        check_result = Target.RESULT_START if self.get_amount() == 0 else check_result
        symbol = check_result['symbol'] + ' ' if check_result is not None else '‣ '
        amount = f"{symbol}{int(self.amount):>{amount_length}} €"
        amount_color = check_result['color'] if check_result is not None else 'yellow'
        check_explanation = ' - ' + str(self.target) if self.target is not None else '' # and check_result != Target.RESULT_OK else ' '
        return colored(amount, amount_color) + ' ' + colored(self.name, 'white') + colored(check_explanation, 'dark_grey')
    
    def __str__(self):
        return self.get_text()


class Envelope:
    def __init__(self, name, elements=None, target=None, parent=None):
        self.name = name
        self.lines = [e for e in elements if isinstance(e, Line)]
        self.children = [e for e in elements if isinstance(e, Envelope)]
        self.target = target
        self.parent = parent

        for e in self.lines + self.children:
            e.set_parent(self)
    
    def set_parent(self, parent):
        self.parent = parent
    
    def add_line(self, line):
        self.lines.append(line)
    
    def add_envelope(self, envelope):
        self.children.append(envelope)
    
    def set_line_amount(self, line_name, amount):
        for l in self.lines:
            if l.key == line_name:
                l.set_amount(amount)
                return True
        for e in self.children:
            if e.set_line_amount(line_name, amount) is True:
                return True
        return False
    
    def get_amount(self, recursive=True):
        self_total = np.sum([l.amount for l in self.lines])
        if recursive:
            self_total += np.sum([e.get_amount(recursive=True) for e in self.children])
        return self_total
    
    def print_tree(self, _indent=0):
        print(' ' * _indent * 4 + colored(f"{str(int(self.get_amount()))} € ", 'blue') + colored(str(self), 'blue', attrs=['bold']))
        max_amount_length = np.max([l.get_amount_length() for l in self.lines]) if self.lines else 1
        for i, line in enumerate(self.lines):
            print(' ' * (_indent * 4 + 4) + ('├─ ' if i + 1 != len(self.lines) else '└─ ') + line.get_text(max_amount_length))
        for env in self.children:
           env.print_tree(_indent + 1)

    def __str__(self):
        return self.name


class Target: # TODO add description to target and show it in the tree
    RESULT_NOK       = {'symbol': '×', 'color': 'red'}
    RESULT_OK        = {'symbol': '✓', 'color': 'green'}
    RESULT_TOLERATED = {'symbol': '≈', 'color': 'yellow'}
    RESULT_INVEST    = {'symbol': '↗', 'color': 'red'}
    RESULT_DEVEST    = {'symbol': '↘', 'color': 'red'}
    RESULT_START     = {'symbol': '↯', 'color': 'cyan'}

    def __init__(self):
        self.parent = None

    def check(self):
        raise NotImplementedError()
    
    def set_parent(self, parent):
        self.parent = parent
    
    def get_amount(self):
        if self.parent is None:
            raise ValueError("Target's parent must be set before checking target.")
        return self.parent.get_amount()


class TargetGlobalRatio(Target):
    def __init__(self, target_ratio, tolerance=0):
        super().__init__()
        self.target_ratio = target_ratio
        self.tolerance = tolerance
    
    def _get_reference(self):
        # Get the tree's root element
        root = self.parent
        while root.parent is not None:
            root = root.parent
        return root.get_amount()
    
    def get_ratio(self):
        total = self._get_reference()
        return 100 * self.get_amount() / total if total > 0 else 0
    
    def check(self):
        ratio = self.get_ratio()
        if ratio < self.target_ratio - self.tolerance / 2:
            return Target.RESULT_INVEST
        elif ratio > self.target_ratio + self.tolerance / 2:
            return Target.RESULT_DEVEST
        return Target.RESULT_OK

    def __str__(self):
        return f'Global ratio {round(self.get_ratio())}% → {self.target_ratio}%'


class TargetRatio(TargetGlobalRatio):
    def _get_reference(self):
        return self.parent.parent.get_amount()
    
    def __str__(self):
        return f'Ratio {round(self.get_ratio())}% → {self.target_ratio}%'


class TargetMin(Target):
    def __init__(self, target_amount, tolerance=0):
        super().__init__()
        self.target_amount = target_amount
        self.tolerance = tolerance

    def check(self):
        if self.parent.get_amount() == 0:
            return Target.RESULT_START
        elif self._operator(self.get_amount(), self.target_amount):
            return Target.RESULT_OK
        elif self._operator(self.get_amount(), self.target_amount, self.tolerance):
            return Target.RESULT_TOLERATED
        return self._nok()
    
    def _operator(self, amount, target, tol=0):
        return amount >= target - tol

    def _nok(self):
        return Target.RESULT_INVEST
    
    def __str__(self):
        return f'Minimum {self.target_amount} €'


class TargetMax(TargetMin):
    def _operator(self, amount, target, tol=0):
        return amount <= target + tol

    def _nok(self):
        return Target.RESULT_DEVEST

    def __str__(self):
        return f'Maximum {self.target_amount} €'


class TargetEqual(TargetMin):
    def _operator(self, amount, target, tol=0):
        return amount >= target - (tol / 2) and amount <= target + (tol / 2)

    def _nok(self):
        return Target.RESULT_NOK

    def __str__(self):
        return f'Target {self.target_amount - self.tolerance}-{self.target_amount + self.tolerance} €'


if __name__ == '__main__':
    patrimoine = Envelope('Patrimoine', elements=[
        Envelope('Court Terme', elements=[
            Envelope('Quotidien', elements=[
                Line("CCP N26", AssetType.CCP, EnvelopeType.CCP, target=TargetMax(500, 100)),
            ]),
            Envelope('Mensuel', elements=[
                Line("CCP Boursorama", AssetType.CCP, EnvelopeType.CCP, target=TargetMax(1000, 1000)),
                Line("CCP Banque Postale", AssetType.CCP, EnvelopeType.CCP, target=TargetMax(1500, 1500))
            ]),
            Envelope('Précaution', elements=[
                Line("LDDS", AssetType.LIVRET, EnvelopeType.LIVRET, key="Livret de Developpement Durable et Solidaire", target=TargetMin(6000)),
            ]),
            Envelope('Projets & Voyages', elements=[
                Line("LDDS", AssetType.LIVRET, EnvelopeType.LIVRET, key="Livret de Developpement Durable et Solidaire", target=TargetMin(2000)),
            ]),
        ]),
        Envelope('Moyen Terme (1-8 ans)', elements=[
            Line("Livret A", AssetType.LIVRET, EnvelopeType.LIVRET, key="LIVRET A", target=TargetMin(20000)),
            Line("Livret Jeune", AssetType.LIVRET, EnvelopeType.LIVRET, key="LIVRET JEUNE", target=TargetMin(1600)),
            Line("Fonds euro Linxea", AssetType.FOND_EURO, EnvelopeType.AV, key="Fonds Euro Nouvelle Generation", target=TargetMin(0)),
        ]),
        Envelope('Long Terme (10+ ans)', elements=[
            Envelope('Tranquille', elements=[
                Line("Fonds euro Linxea", AssetType.FOND_EURO, EnvelopeType.AV, key="Fonds Euro Nouvelle Generation"),
            ]),
            Envelope('Business as usual', elements=[
                Envelope('ETF World', elements=[
                    Line("SP500", AssetType.ETF, EnvelopeType.PEA, key="Amundi PEA S&P 500 UCITS ETF", target=TargetRatio(41, 10)),
                    Line("Russell 2000", AssetType.ETF, EnvelopeType.PEA, key="", target=TargetRatio(9, 4)),
                    Line("Europe 600", AssetType.ETF, EnvelopeType.PEA, key="BNP Paribas Stoxx Europe 600 UCITS ETF Acc", target=TargetRatio(25, 10)),
                    Line("Europe Small Cap", AssetType.ETF, EnvelopeType.PEA, key="", target=TargetRatio(5, 4)),
                    Line("Emerging markets", AssetType.ETF, EnvelopeType.PEA, key="Amundi PEA MSCI Emerging Markets UCITS ETF", target=TargetRatio(14, 10)),
                    Line("Japon", AssetType.ETF, EnvelopeType.PEA, key="", target=TargetRatio(6, 4))
                ]),
            ]),
            Envelope('Croissance verte', elements=[
                Envelope('ETF World ESG', elements=[
                    Line("World ESG", AssetType.ETF, EnvelopeType.AV, key="Amundi MSCI World SRI UCITS ETF DR", target=TargetRatio(50, 10)),
                    Line("USA ESG", AssetType.ETF, EnvelopeType.AV, key="Amundi INDEX MSCI USA SRI UCITS ETF DR", target=TargetRatio(30, 10)),
                    Line("Euro ESG (PEA)", AssetType.ETF, EnvelopeType.PEA, key="Amundi EURO ISTOXX CLIMATE PARIS ALIGNED PAB UCITS ETF DR - EUR (C)", target=TargetRatio(20, 10)),
                    Line("Euro ESG (AV)", AssetType.ETF, EnvelopeType.PEA, key="Amundi INDEX MSCI EUROPE SRI UCITS ETF DR", target=TargetRatio(0)),
                    Line("Emerging markets ESG", AssetType.ETF, EnvelopeType.AV, key="Amundi INDEX MSCI EMERGING MARKETS SRI UCITS ETF DR", target=TargetRatio(10, 10)),
                ]),
                Envelope('Gestion pilotée', elements=[
                    Line("Goodvest", AssetType.PILOTED, EnvelopeType.AV),
                ]),
            ]),
            Envelope('Satellite', elements=[
                Line('Crowdfunding', AssetType.CROWDFUNDING, EnvelopeType.PLATFORM),
                Line('Dividendes', AssetType.STOCK, EnvelopeType.PEA),
                Line('Forets', AssetType.STOCK, EnvelopeType.PEA),
                Line('Autres?', AssetType.STOCK, EnvelopeType.PEA),
            ])
        ]),
        Envelope('Retraite', elements=[
            Line('Prefon PER', AssetType.PILOTED, EnvelopeType.PER),
        ]),
        Envelope('Défense', elements=[
            Line('Or', AssetType.GOLD, EnvelopeType.PHYSICAL, target=TargetGlobalRatio(6, 2)),
            Line('Argent', AssetType.SILVER, EnvelopeType.PHYSICAL, target=TargetGlobalRatio(2, 1)),
            Line('Cryptos', AssetType.CRYPTO, EnvelopeType.WALLET, target=TargetGlobalRatio(2, 1)),
        ]),
        Envelope('Reventes passifs', elements=[
            Line('Moto', AssetType.PASSIVE, EnvelopeType.PHYSICAL, key='Moto Z650'),
        ]),
    ])

    # Fill tree with current valuations fetched from Finary
    match_finary(ff.prepare_session(), patrimoine)

    print("\n---\n")
    patrimoine.print_tree()