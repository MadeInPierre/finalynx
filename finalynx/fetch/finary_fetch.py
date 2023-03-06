import json
import os

from rich.prompt import Confirm
from rich.tree import Tree
from unidecode import unidecode

import finary_api.__main__ as ff
import finary_api.constants
from ..console import console
from ..portfolio.line import Line


def match_line(portfolio, key, amount, node, ignore_orphans, indent=0):
    key, amount = unidecode(key), round(amount)
    node_child = node.add(f"{amount} {key}")
    if not portfolio.set_child_amount(key, amount) and not ignore_orphans:
        node_child.add("[yellow]WARNING: This line did not match with any envelope, attaching to root")
        portfolio.add_child(Line(key, amount=amount))


def finary_fetch(portfolio, force_signin=False, ignore_orphans=False):
    tree = Tree("Finary API", highlight=True, hide_root=True)

    # Let the user reset its credentials and session
    if force_signin:
        if os.path.exists(finary_api.constants.COOKIE_FILENAME):
            os.remove(finary_api.constants.COOKIE_FILENAME)
        if os.path.exists(finary_api.constants.CREDENTIAL_FILE):
            os.remove(finary_api.constants.CREDENTIAL_FILE)

    # Get the user credentials if there's no session yet (through environment variables or manual input)
    if not os.path.exists(finary_api.constants.COOKIE_FILENAME):
        # Skip credential input if it was already set in environment variables
        if os.environ.get("FINARY_EMAIL") and os.environ.get("FINARY_PASSWORD"):
            console.log("Found credentials in environment variables, logging in.")

        # Ask for manual input if credentials and session are missing
        else:
            console.log("Credentials in environment variables not set, asking for manual input.")

            credentials = {}
            if os.path.exists(finary_api.constants.CREDENTIAL_FILE):
                cred_file = open(finary_api.constants.CREDENTIAL_FILE)
                credentials = json.load(cred_file)
            else:
                credentials["email"] = console.input("Enter your Finary [yellow bold]email[/]: ")
                credentials["password"] = console.input("Enter your Finary [yellow bold]password[/]: ", password=True)

                if Confirm.ask(
                    f"Would like to save your credentials in [green]'{finary_api.constants.CREDENTIAL_FILE}'[/]?",
                    default=False,
                    show_default=True,
                ):
                    with open(finary_api.constants.CREDENTIAL_FILE, "w") as f:
                        f.write(json.dumps(credentials, indent=4))

            os.environ["FINARY_EMAIL"] = credentials["email"]
            os.environ["FINARY_PASSWORD"] = credentials["password"]

    # Login to Finary with the existing cookies file or credentials in environment variables and retrieve data
    with console.status("[bold green]Fetching data from Finary..."):
        if os.environ.get("FINARY_EMAIL") and os.environ.get("FINARY_PASSWORD"):
            console.log("Signing in to Finary...")
            result = ff.signin()

            if result is None or result["message"] != "Created":
                console.log(
                    "[red][bold]Failed to signin to Finary![/] Deleting credentials and cookies, please try again.[/]"
                )
                if os.path.exists(finary_api.constants.CREDENTIAL_FILE):
                    os.remove(finary_api.constants.CREDENTIAL_FILE)
                return tree

            console.log(f"Successfully signed in, saving session in '{finary_api.constants.COOKIE_FILENAME}'")
        elif os.path.exists(finary_api.constants.COOKIE_FILENAME):
            console.log("Found cookies file, retrieving session.")
        else:
            console.log("[bold red]No credentials file, environment variables, or cookies file. Skipping fetching.[/]")
            return tree

        # Get session stored in cookies file
        session = ff.prepare_session()

        # Comptes courants, Livrets et Fonds euro
        checkings = ff.get_checking_accounts(session, "1w")["result"]
        savings = ff.get_savings_accounts(session, "1w")["result"]
        fonds = ff.get_fonds_euro(session, "1w")["result"]
        for result, name in zip([checkings, savings, fonds], ["Comptes courants", "Livrets", "Fonds euro"]):
            console.log(f"Fetching {name.lower()}...")
            node = tree.add("[bold]" + str(round(result["timeseries"][-1][1])) + " " + name)
            for k, e in result["distribution"].items():
                match_line(portfolio, k, e["amount"], node, ignore_orphans, indent=1)

        # Autres
        console.log("Fetching other assets...")
        other = ff.get_other_assets(session, "1w")["result"]
        f_other_total = round(other["timeseries"][-1][1])
        node = tree.add("[bold]" + str(round(f_other_total)) + " Autres")
        for item in other["data"]:
            match_line(
                portfolio,
                item["name"],
                item["current_value"],
                node,
                ignore_orphans,
                indent=1,
            )

        # Investissements
        console.log("Fetching investments...")
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
                "generic_assets",
                "loans",
                "crowdlendings",
            ]:
                for item in account[category]:
                    match_line(
                        portfolio,
                        item["security"]["name"],
                        item["current_value"],
                        node_account,
                        ignore_orphans,
                        indent=2,
                    )

        # Immobilier
        console.log("Fetching real estate...")
        real_estate = ff.get_real_estates(session, "1w")["result"]
        f_re_total = round(real_estate["total"]["amount"])
        node = tree.add("[bold]" + str(round(f_re_total)) + " Immobilier")

        for item in real_estate["data"]["real_estates"]:
            match_line(
                portfolio,
                item["description"],
                item["current_value"],
                node,
                ignore_orphans,
                indent=1,
            )

        for item in real_estate["data"]["scpis"]:
            match_line(
                portfolio,
                item["scpi"]["name"],
                item["current_value"],
                node,
                ignore_orphans,
                indent=1,
            )

    # Delete login variables just in case
    if os.environ.get("FINARY_EMAIL"):
        os.environ.pop("FINARY_EMAIL")
    if os.environ.get("FINARY_PASSWORD"):
        os.environ.pop("FINARY_PASSWORD")

    console.log("Done fetching Finary data.")
    return tree
