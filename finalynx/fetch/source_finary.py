import json
import os
from typing import Any
from typing import Dict
from typing import Optional

import finary_uapi.__main__ as ff
import finary_uapi.constants
import finary_uapi.user_portfolio
from requests import Session
from rich.prompt import Confirm
from rich.tree import Tree

from ..config import get_active_theme as TH
from ..console import console
from .source_base import SourceBase


class SourceFinary(SourceBase):
    """Wrapper class for the `finary_uapi` package."""

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

    def __init__(self, force_signin: bool = False, name: str = "Finary") -> None:
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

        :param clear_cache: Delete cached data to immediately fetch data online, defaults to False
        :param force_signin: Delete all saved credentials, cookies and cache files before logging in again, defaults to False
        :param ignore_orphans: If a line in your account is not referenced in your {class}`Portfolio <finalynx.portfolio.portfolio.Portfolio>`
        then don't attach it to the root (used as a reminder), defaults to False
        :returns: Returns a tree view of all fetched investments, which can be printed to the console to make sure
        everything was correctly found.
        """
        super().__init__(name)
        self.force_signin = force_signin

    def _authenticate(self) -> Optional[Session]:
        """Internal method used to signin and retrieve a session from Finary.
        Called by `_fetch_data` once, only exists for better logic separation.
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
                self._log("Found credentials in environment variables, logging in.")

            # Ask for manual input if credentials and session are missing
            else:
                credentials = {}
                if os.path.exists(finary_uapi.constants.CREDENTIAL_FILE):
                    self._log("Found saved credentials, logging in.")

                    cred_file = open(finary_uapi.constants.CREDENTIAL_FILE)
                    credentials = json.load(cred_file)
                else:
                    self._log("Credentials in environment variables not set, asking for manual input.")

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
        if os.environ.get("FINARY_EMAIL") and os.environ.get("FINARY_PASSWORD"):
            with console.status(f"[bold {TH().ACCENT}]Signing in to Finary...", spinner_style=TH().ACCENT):
                result = ff.signin()
                self._log("Signed in to Finary.")

            if result is None or result["message"] != "Created":
                self._log(
                    "[red][bold]Failed to signin to Finary![/] Deleting credentials and cookies, please try again.[/]"
                )
                if os.path.exists(finary_uapi.constants.CREDENTIAL_FILE):
                    os.remove(finary_uapi.constants.CREDENTIAL_FILE)
                return None

            self._log(f"Successfully signed in, saving session in '{finary_uapi.constants.COOKIE_FILENAME}'")
        elif os.path.exists(finary_uapi.constants.COOKIE_FILENAME):
            self._log("Found cookies file, retrieving session.")
        else:
            self._log("[bold red]No credentials file, environment variables, or cookies file. Skipping fetching.[/]")
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
        """Overridden method used to fetch every investment in your Finary account.
        :returns: A dictionary of all fetched investments (name:amount format). This method
        also populates the `tree` instance with a hierarchical view of the fetched information.
        The `tree` instance can be displayed in the console to make sure everything was retrieved.
        """

        # Retrieve the user session from cache, environment variables, or manual login
        session = self._authenticate()
        if not session:
            raise ValueError("Finary signin failed.")

        # Call the API and parse the response into `FetchLine` instances
        with console.status(f"[bold {TH().ACCENT}]Fetching investments from Finary...", spinner_style=TH().ACCENT):
            response = ff.get_holdings_accounts(session)
            if response["message"] == "OK":
                for dict_account in response["result"]:
                    self._process_account(dict_account, tree)

    def _process_account(self, dict_account: Dict[str, Any], tree: Tree) -> None:
        account_name = dict_account["name"]
        node = tree.add(account_name)

        for item in dict_account["fiats"]:
            self._register_fetchline(
                tree_node=node,
                name=account_name,
                id=item["id"],
                account=dict_account["institution"]["name"],
                amount=item["display_current_value"],
                currency=item["fiat"]["symbol"],
            )

        for item in dict_account["securities"]:
            self._register_fetchline(
                tree_node=node,
                name=item["security"]["name"],
                id=item["id"],
                account=account_name,
                amount=item["display_current_value"],
                currency=item["security"]["display_currency"]["symbol"],
            )

        for item in dict_account["crowdlendings"]:
            self._register_fetchline(
                tree_node=node,
                name=item["name"],
                id=item["id"],
                account=account_name,
                amount=item["display_current_price"],
                currency=item["currency"]["symbol"],
            )

        for item in dict_account["cryptos"]:
            self._register_fetchline(
                tree_node=node,
                name=item["crypto"]["name"],
                id=item["id"],
                account=account_name,
                amount=item["display_current_value"],
                currency=item["buying_price_currency"]["symbol"],
            )

        for item in dict_account["fonds_euro"]:
            self._register_fetchline(
                tree_node=node,
                name=item["name"],
                id=item["id"],
                account=account_name,
                amount=item["display_current_value"],
                currency=dict_account["display_currency"]["symbol"],
            )

        for item in dict_account["precious_metals"]:
            self._register_fetchline(
                tree_node=node,
                name=item["precious_metal"]["name"],
                id=item["id"],
                account=account_name,
                amount=item["display_current_value"],
                currency=item["precious_metal"]["display_currency"]["symbol"],
            )

        for item in dict_account["startups"]:
            self._register_fetchline(
                tree_node=node,
                name=item["startup"]["name"],
                id=item["id"],
                account=account_name,
                amount=item["display_current_value"],
                currency=item["currency"]["symbol"],
            )

        for item in dict_account["scpis"]:
            self._register_fetchline(
                tree_node=node,
                name=item["scpi"]["name"],
                id=item["id"],
                account=account_name,
                amount=item["display_current_value"],
                currency=item["scpi"]["display_currency"]["symbol"],
            )

        for item in dict_account["generic_assets"]:
            self._register_fetchline(
                tree_node=node,
                name=item["name"],
                id=item["id"],
                account=account_name,
                amount=item["display_current_value"],
                currency=item["currency"]["symbol"],
            )

        for item in dict_account["real_estates"]:
            self._register_fetchline(
                tree_node=node,
                name=item["description"],
                id=item["id"],
                account=account_name,
                amount=item["display_current_value"],
                currency=dict_account["display_currency"]["symbol"],
            )

        for item in dict_account["loans"]:
            self._register_fetchline(
                tree_node=node,
                name=account_name,
                id=item["id"],
                account=account_name,
                amount=-round(dict_account["display_balance"]),
                currency=dict_account["display_currency"]["symbol"],
            )
