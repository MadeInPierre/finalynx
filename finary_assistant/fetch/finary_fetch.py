import finary_api.__main__ as ff
from unidecode import unidecode
from rich.tree import Tree
from rich.prompt import Prompt, Confirm
from ..console import console
from ..portfolio.line import Line
import os
import json


def finary_fetch(portfolio, ignore_orphans=False):  # TODO cleanup file path management?
    def match_line(portfolio, key, amount, node, indent=0):
        key, amount = unidecode(key), round(amount)
        node_child = node.add(f"{amount} {key}")
        if not portfolio.set_child_amount(key, amount) and not ignore_orphans:
            node_child.add(
                "[yellow]WARNING: This line did not match with any envelope, attaching to root"
            )
            portfolio.add_child(Line(key, amount=amount))

    tree = Tree("Finary API", highlight=True, hide_root=True)

    local_directory_path = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(local_directory_path, "credentials.json")
    current_cookies_path = os.path.join(
        os.path.abspath(os.getcwd()), "localCookiesMozilla.txt"
    )
    local_cookies_path = os.path.join(local_directory_path, "localCookiesMozilla.txt")

    # Manage the credentials file creation and signin
    if not os.environ.get("FINARY_EMAIL") or not os.environ.get("FINARY_PASSWORD"):
        credentials = {}
        if os.path.exists(credentials_path):
            cred_file = open(credentials_path, "r")
            credentials = json.load(cred_file)
        else:
            credentials["email"] = console.input("Your Finary [yellow bold]email[/]: ")
            credentials["password"] = console.input(
                "Your Finary [yellow bold]password[/]: ", password=True
            )

            if Confirm.ask(f"Would like to save your credentials in '{credentials_path}'?"):
                with open(credentials_path, "w") as f:
                    f.write(json.dumps(credentials, indent=4))

        os.environ["FINARY_EMAIL"] = credentials["email"]
        os.environ["FINARY_PASSWORD"] = credentials["password"]

    # Login to Finary
    with console.status("[bold green]Fetching data from Finary..."):
        if os.path.exists(local_cookies_path):
            os.rename(local_cookies_path, current_cookies_path)
        else:
            console.log(f"Signing in to Finary...")
            result = ff.signin()
            if result is None or result["message"] != "Created":
                console.log("[bold red]Signin to Finary failed! Skipping fetch.[/]")
                os.remove(credentials_path)
                return tree
            console.log("Successfully signed in")
        session = ff.prepare_session()

        # Comptes courants, Livrets et Fonds euro
        checkings = ff.get_checking_accounts(session, "1w")["result"]
        savings = ff.get_savings_accounts(session, "1w")["result"]
        fonds = ff.get_fonds_euro(session, "1w")["result"]
        for result, name in zip(
            [checkings, savings, fonds], ["Comptes courants", "Livrets", "Fonds euro"]
        ):
            console.log(f"Fetching {name.lower()}...")
            node = tree.add(
                "[bold]" + str(round(result["timeseries"][-1][1])) + " " + name
            )
            for k, e in result["distribution"].items():
                match_line(portfolio, k, e["amount"], node, indent=1)

        # Autres
        console.log(f"Fetching other assets...")
        other = ff.get_other_assets(session, "1w")["result"]
        f_other_total = round(other["timeseries"][-1][1])
        node = tree.add("[bold]" + str(round(f_other_total)) + " Autres")
        for item in other["data"]:
            match_line(portfolio, item["name"], item["current_value"], node, indent=1)

        # Investissements
        console.log(f"Fetching investments...")
        investments = ff.get_portfolio_investments(session)["result"]
        f_invest_total = round(investments["total"]["amount"])
        node = tree.add("[bold]" + str(round(f_invest_total)) + " Investissements")
        for account in investments["accounts"]:
            node_account = node.add("[bold]Account: " + account["name"])
            for category in [
                "fiats",
                "securities",
                "cryptos",
                "fonds_euro",
                "startups",
                "precious_metals",
                "scpis",
                "generic_assets",
                "real_estates",
                "loans",
                "crowdlendings",
            ]:
                for item in account[category]:
                    match_line(
                        portfolio,
                        item["security"]["name"],
                        item["current_value"],
                        node_account,
                        indent=2,
                    )

    # Delete login variables just in case
    if os.environ.get("FINARY_EMAIL"):
        os.environ.pop("FINARY_EMAIL")
    if os.environ.get("FINARY_PASSWORD"):
        os.environ.pop("FINARY_PASSWORD")

    # Move cookies to this folder to find it next time
    if os.path.exists(current_cookies_path):
        os.rename(current_cookies_path, local_cookies_path)

    console.log("Done fetching Finary data.")
    return tree
