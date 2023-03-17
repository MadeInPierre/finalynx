import datetime
import json
import os
from typing import Dict

from rich.prompt import Confirm
from rich.tree import Tree
from unidecode import unidecode

import finary_api.__main__ as ff  # type: ignore
import finary_api.constants  # type: ignore
from ..console import console
from ..portfolio.line import Line
from ..portfolio.portfolio import Portfolio

CACHE_FILENAME = os.path.join(os.path.dirname(__file__), "finary_data.json")
MAX_CACHE_HOURS = 1


# TODO Refactor in a class
def finary_fetch(portfolio: Portfolio, force_signin: bool = False, ignore_orphans: bool = False) -> Tree:
    """Wrapper function for the `finary_api` package.

    This function manages all interactions with your Finary account, namely:
    1. **Authentication**: The function starts by signing you in with the following sequence of attempts:
        - First, the function looks for environment variables named `FINARY_EMAIL` and `FINARY_PASSWORD`
          containing your credentials. If those are set, they will take priority over all other signin methods.
        - Second, if a file named `localCookiesMozilla.txt` already exists in this same directory (which
          contains the session of a previous signin), it will skip the login step and retrieve the saved sessions.
        - Third, if neither the environment variables nor the cookies file exist, the function will manually ask
          for the credentials in the console.
    2. **Fetching**: Once the session is active, all investments declared in Finary are fetched.
    3. **Populating the tree:** Finally, each fetched investment is matched against either the `name` or `key`
    value of each `Line` object defined in your `Portfolio` and updated in the tree.

    ```{note}
    Finalynx will ask you if you want to save two files:
    - `credentials.json`: This file would store your credentials in a plain text file, which might be used by
      `finary_api` to refresh your session (to be confirmed). However, this is not recommended since only storing
      the session is more secure and you can always enter your credentials again from occasionally.
    - `localCookiesMozilla.txt`: This file stores the session created after a successful login (without your
    plain credentials). It is recommended to save it if you don't want to enter your credentials on each run.

    You can run Finalynx with the `-f` or `--force-signin` option to delete all files and start over:
    {code}`python your_config.py --force-signin`
    ```

    :param portfolio: Your {class}`Portfolio <finalynx.portfolio.portfolio.Portfolio>` tree (must be already fully defined).
    :param force_signin: Delete all saved credentials and cookies before logging in again, defaults to False
    :param ignore_orphans: If a line in your account is not referenced in your {class}`Portfolio <finalynx.portfolio.portfolio.Portfolio>`
    then don't attach it to the root (used as a reminder), defaults to False
    :returns: Returns a tree view of all fetched investments, which can be printed to the console to make sure
    everything was correctly found.
    """

    def match_line(
        portfolio: Portfolio, key: str, amount: float, node: Tree, lines_dict: Dict[str, int], ignore_orphans: bool
    ) -> None:
        key, amount = unidecode(key), round(amount)
        node_child = node.add(f"{amount} {key}")
        lines_dict[key] = amount
        if not portfolio.set_child_amount(key, amount) and not ignore_orphans:
            node_child.add("[yellow]WARNING: This line did not match with any envelope, attaching to root")
            portfolio.add_child(Line(key, amount=amount))

    tree = Tree("Finary API", highlight=True, hide_root=True)
    lines_dict: Dict[str, int] = _get_cache()

    if lines_dict:
        for key, value in lines_dict.items():
            match_line(portfolio, key, value, tree, lines_dict, ignore_orphans)
        return tree

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
                match_line(portfolio, k, e["amount"], node, lines_dict, ignore_orphans)

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
                lines_dict,
                ignore_orphans,
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
                        lines_dict,
                        ignore_orphans,
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
                lines_dict,
                ignore_orphans,
            )

        for item in real_estate["data"]["scpis"]:
            match_line(
                portfolio,
                item["scpi"]["name"],
                item["current_value"],
                node,
                lines_dict,
                ignore_orphans,
            )

    # Delete login variables just in case
    if os.environ.get("FINARY_EMAIL"):
        os.environ.pop("FINARY_EMAIL")
    if os.environ.get("FINARY_PASSWORD"):
        os.environ.pop("FINARY_PASSWORD")

    # Save
    console.log("Saving fetched data in '{CACHE_FILENAME}'")
    _save_cache(lines_dict)

    console.log("Done fetching Finary data.")
    return tree


def _save_cache(lines_dict: Dict[str, int]) -> None:
    """Save the fetched data locally to work offline and reduce the amoutn of calls to the API.
    :param tree: Generated tree object containing all information
    """
    # Save current date and time to a JSON file with the fetched data
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"last_updated": current_time, "lines": lines_dict}
    with open(CACHE_FILENAME, "w") as f:
        json.dump(data, f, indent=4)


def _get_cache() -> Dict[str, int]:
    """Attempt to retrieve the cached data. Check if more than an hour has passed since the last update.
    :returns: A key:amount dictionary if the cache file is less than an hour old, None otherwise.
    """

    # Abort retrieving cache if the file doesn't exist
    if not os.path.exists(CACHE_FILENAME):
        console.log("No cache file found, fetching data.")
        return {}

    # Parse the JSON content
    with open(CACHE_FILENAME) as f:
        data = json.load(f)

    # Return the cached content if the cache file is less than the maximum age
    last_updated = datetime.datetime.strptime(data["last_updated"], "%Y-%m-%d %H:%M:%S")
    time_diff = datetime.datetime.now() - last_updated
    hours_passed = int(time_diff.total_seconds() // 3600)

    if hours_passed < MAX_CACHE_HOURS:
        console.log(f"Using recently cached data ({hours_passed}h old < {MAX_CACHE_HOURS}h max)")
        lines: Dict[str, int] = data["lines"]
        return lines
    console.log("Fetching data (cache file is {hours_passed}h old > {MAX_CACHE_HOURS}h max)")
    return {}
