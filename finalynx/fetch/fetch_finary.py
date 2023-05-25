import json
import os
from typing import Optional

import finary_uapi.__main__ as ff
import finary_uapi.constants
import finary_uapi.user_portfolio
from requests import Session
from rich.prompt import Confirm
from rich.tree import Tree

from ..console import console
from ..portfolio.folder import Portfolio
from .fetch_base import FetchBase


class FetchFinary(FetchBase):
    """Wrapper class for the `finary_uapi` package."""

    SOURCE_NAME = "Finary"

    _categories = [
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
    ]

    def __init__(
        self,
        portfolio: Portfolio,
        clear_cache: bool = False,
        force_signin: bool = False,
        ignore_orphans: bool = False,
    ) -> None:
        """This class manages all interactions with your Finary account, namely:
        1. **Authentication**: The function starts by signing you in with the following sequence of attempts:
            - First, the function looks for environment variables named `FINARY_EMAIL` and `FINARY_PASSWORD`
            containing your credentials. If those are set, they will take priority over all other signin methods.
            - Second, if a file named `finary_cookies.txt` already exists in this same directory (which
            contains the session of a previous signin), it will skip the login step and retrieve the saved sessions.
            - Third, if neither the environment variables nor the cookies file exist, the function will manually ask
            for the credentials in the console.
        2. **Fetch the data**: Once the session is active, all investments declared in Finary are fetched.
        3. **Populate the portfolio:** Finally, each fetched investment is matched against either the `name` or `key`
        value of each `Line` object defined in your `Portfolio` and updated in the tree.
        4. **Cache the data:** Once the data has been fetched, all data is saved to a local file to reduce the frequency
        of calls to Finary API and enable the usage of this module offline temporarily.

        ```{note}
        Finalynx will ask you if you want to save two files:
        - `finary_credentials.json`: This file would store your credentials in a plain text file, which might be
        used by `finary_uapi` to refresh your session (to be confirmed). However, this is not recommended since
        only storing the session is more secure and you can always enter your credentials again from occasionally.
        - `finary_cookies.txt`: This file stores the session created after a successful login (without your
        plain credentials). It is recommended to save it if you don't want to enter your credentials on each run.

        You can run Finalynx with the `-f` or `--force-signin` option to delete all files and start over.
        ```

        :param portfolio: Your {class}`Portfolio <finalynx.portfolio.portfolio.Portfolio>` tree (must be already fully defined).
        :param clear_cache: Delete cached data to immediately fetch data online, defaults to False
        :param force_signin: Delete all saved credentials, cookies and cache files before logging in again, defaults to False
        :param ignore_orphans: If a line in your account is not referenced in your {class}`Portfolio <finalynx.portfolio.portfolio.Portfolio>`
        then don't attach it to the root (used as a reminder), defaults to False
        :returns: Returns a tree view of all fetched investments, which can be printed to the console to make sure
        everything was correctly found.
        """
        super().__init__(self.SOURCE_NAME, portfolio, clear_cache, force_signin, ignore_orphans)

    def _authenticate(self) -> Optional[Session]:
        """Internal method used to signin and retrieve a session from Finary.
        :returns: A session for fetching data if everything worked, None otherwise.
        """

        # Let the user reset its credentials and session
        if self.force_signin:
            if os.path.exists(finary_uapi.constants.COOKIE_FILENAME):
                os.remove(finary_uapi.constants.COOKIE_FILENAME)
            if os.path.exists(finary_uapi.constants.CREDENTIAL_FILE):
                if not Confirm.ask("Reuse saved credentials? Otherwise, they will also be deleted.", default=True):
                    os.remove(finary_uapi.constants.CREDENTIAL_FILE)

        # Get the user credentials if there's no session yet (through environment variables or manual input)
        if not os.path.exists(finary_uapi.constants.COOKIE_FILENAME):
            # Skip credential input if it was already set in environment variables
            if os.environ.get("FINARY_EMAIL") and os.environ.get("FINARY_PASSWORD"):
                console.log("Found credentials in environment variables, logging in.")

            # Ask for manual input if credentials and session are missing
            else:
                credentials = {}
                if os.path.exists(finary_uapi.constants.CREDENTIAL_FILE):
                    console.log("Found saved credentials, logging in.")

                    cred_file = open(finary_uapi.constants.CREDENTIAL_FILE)
                    credentials = json.load(cred_file)
                else:
                    console.log("Credentials in environment variables not set, asking for manual input.")

                    credentials["email"] = console.input("Enter your Finary [yellow bold]email[/]: ")
                    credentials["password"] = console.input(
                        "Enter your Finary [yellow bold]password[/]: ", password=True
                    )

                    if Confirm.ask(
                        f"Would like to save your credentials in [green]'{finary_uapi.constants.CREDENTIAL_FILE}'[/]?",
                        default=False,
                        show_default=True,
                    ):
                        with open(finary_uapi.constants.CREDENTIAL_FILE, "w") as f:
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
                    if os.path.exists(finary_uapi.constants.CREDENTIAL_FILE):
                        os.remove(finary_uapi.constants.CREDENTIAL_FILE)
                    return None

                console.log(f"Successfully signed in, saving session in '{finary_uapi.constants.COOKIE_FILENAME}'")
            elif os.path.exists(finary_uapi.constants.COOKIE_FILENAME):
                console.log("Found cookies file, retrieving session.")
            else:
                console.log(
                    "[bold red]No credentials file, environment variables, or cookies file. Skipping fetching.[/]"
                )
                return None

            # Get session stored in cookies file
            session: Session = ff.prepare_session()

            # Delete login variables just in case
            if os.environ.get("FINARY_EMAIL"):
                os.environ.pop("FINARY_EMAIL")
            if os.environ.get("FINARY_PASSWORD"):
                os.environ.pop("FINARY_PASSWORD")

            return session

    def _fetch_data(self, tree: Tree) -> None:
        """Internal method used to fetch every investment in your Finary account.
        :returns: A dictionary of all fetched investments (name:amount format). This method
        also populates the `tree` instance with a hierarchical view of the fetched information.
        The `tree` instance can be displayed in the console to make sure everything was retrieved.
        """

        # Retrieve the user session from cache, environment variables, or manual login
        session = self._authenticate()
        if not session:
            raise ValueError("Finary signin failed.")

        # Simple utility function because fetching Finary data takes multiple steps
        def start_step(step_name: str, tree_node: Tree) -> Tree:
            console.log(f"Fetching {step_name.lower()}...")
            return tree_node.add(f"[bold]{step_name}")

        # Checkings
        node = start_step("Checkings", tree)
        for e in ff.get_checking_accounts(session, "1w")["result"]["data"]:
            self._register_fetchline(
                tree_node=node,
                name=e["name"],
                id=e["id"],
                account=e["institution"]["name"],
                amount=e["display_balance"],
                currency=e["display_currency"]["symbol"],
            )

        # Savings
        node = start_step("Savings", tree)
        for e in ff.get_savings_accounts(session, "1w")["result"]["data"]:
            self._register_fetchline(
                tree_node=node,
                name=e["name"],
                id=e["id"],
                account=e["institution"]["name"],
                amount=e["display_balance"],
                currency=e["display_currency"]["symbol"],
            )

        # Fonds euro
        node = start_step("Fonds euro", tree)
        for e in ff.get_fonds_euro(session, "1w")["result"]["data"]:
            self._register_fetchline(
                tree_node=node,
                name=e["name"],
                id=e["id"],
                account=e["account"]["name"],
                amount=e["display_current_value"],
                currency=e["account"]["display_currency"]["symbol"],
            )

        # Others
        node = start_step("Others", tree)
        for e in ff.get_other_assets(session, "1w")["result"]["data"]:
            self._register_fetchline(
                tree_node=node,
                name=e["name"],
                id=e["id"],
                account=e["account"]["name"],
                amount=e["display_current_value"],
                currency=e["account"]["display_currency"]["symbol"],
            )

        # Precious metals
        node = start_step("Precious metals", tree)
        for e in ff.get_user_precious_metals(session)["result"]:
            self._register_fetchline(
                tree_node=node,
                name=e["precious_metal"]["name"],
                id=e["id"],
                account=e["account"]["name"],
                amount=e["display_current_value"],
                currency=e["precious_metal"]["display_currency"]["symbol"],
            )

        # Investments
        node = start_step("Investments", tree)
        for account in ff.get_portfolio_investments(session)["result"]["accounts"]:
            node_account = node.add(f"[bold]Account: {account['name']}")
            for e in account["securities"]:
                self._register_fetchline(
                    tree_node=node_account,
                    name=e["security"]["name"],
                    id=e["id"],
                    account=account["name"],
                    amount=e["display_current_value"],
                    currency=e["security"]["display_currency"]["symbol"],
                )

        # Cryptos
        node = start_step("Cryptos", tree)
        for account in finary_uapi.user_portfolio.get_portfolio_cryptos(session)["result"]["accounts"]:
            node_account = node.add(f"[bold]Account: {account['name']}")
            for e in account["cryptos"]:
                self._register_fetchline(
                    tree_node=node_account,
                    name=e["crypto"]["name"],
                    id=e["id"],
                    account=account["name"],
                    amount=e["display_current_value"],
                    currency=e["buying_price_currency"]["symbol"],
                )

        # Real estate
        node = start_step("Real estate", tree)
        real_estate = ff.get_real_estates(session, "1w")["result"]["data"]
        for e in real_estate["real_estates"]:
            self._register_fetchline(
                tree_node=node,
                name=e["description"],
                id=e["id"],
                account=e["account"]["name"],
                amount=e["display_current_value"],
                currency=e["account"]["display_currency"]["symbol"],
            )
        for e in real_estate["scpis"]:
            self._register_fetchline(
                tree_node=node,
                name=e["scpi"]["name"],
                id=e["id"],
                account=e["account"]["name"],
                amount=e["display_current_value"],
                currency=e["account"]["display_currency"]["symbol"],
            )

        # Loans
        node = start_step("Loans", tree)
        for e in ff.get_loans(session)["result"]["data"]:
            self._register_fetchline(
                tree_node=node,
                name=e["name"],
                id=e["id"],
                account=e["account"]["name"],
                amount=-e["account"]["display_balance"],
                currency=e["display_currency"]["symbol"],
            )

        # Credit accounts
        node = start_step("Credit accounts", tree)
        for e in ff.get_credit_accounts(session)["result"]["data"]:
            self._register_fetchline(
                tree_node=node,
                name=e["name"],
                id=e["id"],
                account=e["name"],
                amount=-e["display_balance"],
                currency=e["display_currency"]["symbol"],
            )

        # Crowdlendings
        node = start_step("Crowdlendings", tree)
        for account in ff.get_portfolio_crowdlendings(session)["result"]["accounts"]:
            node_account = node.add(f"[bold]Account: {account['name']}")
            for e in account["crowdlendings"]:
                self._register_fetchline(
                    tree_node=node_account,
                    name=e["name"],
                    id=e["id"],
                    account=account["name"],
                    amount=e["display_current_value"],
                    currency=e["currency"]["symbol"],
                )

        # Startups
        node = start_step("Startups", tree)
        real_estate = ff.get_user_startups(session)["result"]
        for e in real_estate["startups"]:
            self._register_fetchline(
                tree_node=node,
                name=e["name"],
                amount=e["current_value"],
                id=e["slug"],
                account=e["name"],
                currency="€",  # no currency info available
            )
