import finary_api as ff # noqa
from unidecode import unidecode
from rich.tree import Tree
from ..console import console
from ..patrimoine.line import Line

def finary_fetch(patrimoine):
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