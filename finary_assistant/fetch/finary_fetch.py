import finary_api.__main__ as ff
import finary_api.constants
from unidecode import unidecode
from rich.tree import Tree
from rich.prompt import Prompt, Confirm
from ..console import console
from ..portfolio.line import Line
import os
import json


def match_line(portfolio, key, amount, node, ignore_orphans, indent=0):
    key, amount = unidecode(key), round(amount)
    node_child = node.add(f"{amount} {key}")
    if not portfolio.set_child_amount(key, amount) and not ignore_orphans:
        node_child.add(
            "[yellow]WARNING: This line did not match with any envelope, attaching to root"
        )
        portfolio.add_child(Line(key, amount=amount))


def finary_fetch(portfolio, force_signin=False, ignore_orphans=False):
    tree = Tree("Finary API", highlight=True, hide_root=True)

    # Let the user reset its credentials and session
    if force_signin:
        if os.path.exists(finary_api.constants.COOKIE_FILENAME):
            os.remove(finary_api.constants.COOKIE_FILENAME)
        if os.path.exists(finary_api.constants.CREDENTIAL_FILE):
            os.remove(finary_api.constants.CREDENTIAL_FILE)

    # Manage the credentials file creation and signin
    if not os.path.exists(finary_api.constants.COOKIE_FILENAME):
        if not os.environ.get("FINARY_EMAIL") or not os.environ.get("FINARY_PASSWORD"):
            credentials = {}
            if os.path.exists(finary_api.constants.CREDENTIAL_FILE):
                cred_file = open(finary_api.constants.CREDENTIAL_FILE, "r")
                credentials = json.load(cred_file)
            else:
                credentials["email"] = console.input(
                    "Your Finary [yellow bold]email[/]: "
                )
                credentials["password"] = console.input(
                    "Your Finary [yellow bold]password[/]: ", password=True
                )

                if Confirm.ask(
                    f"Would like to save your credentials in '{finary_api.constants.CREDENTIAL_FILE}'?"
                ):
                    with open(finary_api.constants.CREDENTIAL_FILE, "w") as f:
                        f.write(json.dumps(credentials, indent=4))

            os.environ["FINARY_EMAIL"] = credentials["email"]
            os.environ["FINARY_PASSWORD"] = credentials["password"]

    # Login to Finary
    with console.status("[bold green]Fetching data from Finary..."):
        if not os.path.exists(finary_api.constants.COOKIE_FILENAME):
            console.log(f"Signing in to Finary...")
            result = ff.signin()
            if result is None or result["message"] != "Created":
                console.log("[bold red]Signin to Finary failed! Skipping fetch.[/]")
                os.remove(finary_api.constants.CREDENTIAL_FILE)
                return tree
            console.log("Successfully signed in")
        else:
            console.log("Found existing cookies file, skipping signin")
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
                match_line(portfolio, k, e["amount"], node, ignore_orphans, indent=1)

        # Autres
        console.log(f"Fetching other assets...")
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
                        ignore_orphans,
                        indent=2,
                    )

    # Delete login variables just in case
    if os.environ.get("FINARY_EMAIL"):
        os.environ.pop("FINARY_EMAIL")
    if os.environ.get("FINARY_PASSWORD"):
        os.environ.pop("FINARY_PASSWORD")

    console.log("Done fetching Finary data.")
    return tree
