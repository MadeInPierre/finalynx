import datetime
import json
import os
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from requests import Session
from rich.prompt import Confirm
from rich.tree import Tree
from unidecode import unidecode

import finary_api.__main__ as ff
import finary_api.constants
import finary_api.user_portfolio
from ..console import console
from ..portfolio.line import Line
from ..portfolio.portfolio import Portfolio
from .fetch import Fetch


class FetchFinary(Fetch):  # TODO update docstrings
    """Wrapper class for the `finary_api` package."""

    CACHE_FILENAME = "finary_data.json"

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
        self, portfolio: Portfolio, clear_cache: bool = False, force_signin: bool = False, ignore_orphans: bool = False
    ) -> None:
        """This class manages all interactions with your Finary account, namely:
        1. **Authentication**: The function starts by signing you in with the following sequence of attempts:
            - First, the function looks for environment variables named `FINARY_EMAIL` and `FINARY_PASSWORD`
            containing your credentials. If those are set, they will take priority over all other signin methods.
            - Second, if a file named `localCookiesMozilla.txt` already exists in this same directory (which
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
        - `credentials.json`: This file would store your credentials in a plain text file, which might be used by
        `finary_api` to refresh your session (to be confirmed). However, this is not recommended since only storing
        the session is more secure and you can always enter your credentials again from occasionally.
        - `localCookiesMozilla.txt`: This file stores the session created after a successful login (without your
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
        super().__init__(portfolio, self.CACHE_FILENAME)
        self.clear_cache = clear_cache
        self.force_signin = force_signin
        self.ignore_orphans = ignore_orphans

    def fetch(self) -> Tree:
        """:returns: A `Tree` object from the `rich` package used to display what has been fetched."""

        # Remove the cached Finary data if asked by the user
        if self.clear_cache and os.path.exists(self.cache_fullpath):
            os.remove(self.cache_fullpath)

        # This will hold a key:amount dictionary of all lines found in the Finary account
        lines_list: List[Dict[str, Any]] = self._get_cache()  # try to get the data in the cache first
        tree = Tree("Finary API", highlight=True, hide_root=True)

        # If the cache is not empty, Match all lines to the portfolio hierarchy
        if lines_list:
            for line in lines_list:
                self._match_line([], tree, key=line["key"], id=line["id"], amount=line["amount"])

        # If there's no valid cache, signin and fetch the data online
        else:
            session = self._authenticate()
            if not session:
                return Tree("Finary signin failed.")

            try:
                lines_list, tree = self._fetch_data(session, tree)
            except Exception:
                console.log("[red bold]Error: Couldn't fetch data, please try using the `-f` option to signin again.")
                return tree

            # Save what has been found in a cache file for offline use and better performance at next launch
            self._save_cache(lines_list)

        # Return a rich tree to be displayed in the console as a recap of what has been fetched
        console.log("Done fetching Finary data.")
        return tree

    def _authenticate(self) -> Optional[Session]:
        """Internal method used to signin and retrieve a session from Finary.
        :returns: A session for fetching data if everything worked, None otherwise.
        """

        # Let the user reset its credentials and session
        if self.force_signin:
            if os.path.exists(finary_api.constants.COOKIE_FILENAME):
                os.remove(finary_api.constants.COOKIE_FILENAME)
            if os.path.exists(finary_api.constants.CREDENTIAL_FILE):
                if not Confirm.ask("Reuse saved credentials? Otherwise, they will also be deleted.", default=True):
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
                    credentials["password"] = console.input(
                        "Enter your Finary [yellow bold]password[/]: ", password=True
                    )

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
                    return None

                console.log(f"Successfully signed in, saving session in '{finary_api.constants.COOKIE_FILENAME}'")
            elif os.path.exists(finary_api.constants.COOKIE_FILENAME):
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

    def _fetch_data(self, session: Session, tree: Tree) -> Tuple[List[Dict[str, Any]], Tree]:
        """Internal method used to fetch every investment in your Finary account.
        :returns: A dictionary of all fetched investments (name:amount format), and a `Tree`
        instance which can be displayed in the console to make sure everything was retrieved.
        """
        # Create a rich Tree to display the fetched data nicely
        lines_list: List[Dict[str, Any]] = []

        # Common fetching procedure for multiple sources
        def _process(
            step_name: str,
            function: Callable[..., Dict[str, Any]],
            callback: Callable[[Dict[str, Any]], Tuple[str, str, int]],
            period: bool = True,
        ) -> None:
            console.log(f"Fetching {step_name.lower()}...")
            node = tree.add(f"[bold]{step_name}")
            result = function(session, "1w")["result"]["data"] if period else function(session)["result"]

            for e in result:
                key, id, amount = callback(e)
                self._match_line(lines_list, node, key, id, round(amount))

        # Process similar sources together
        _process("Checkings", ff.get_checking_accounts, lambda e: (e["name"], e["id"], e["fiats"][0]["current_value"]))
        _process("Savings", ff.get_savings_accounts, lambda e: (e["name"], e["id"], e["fiats"][0]["current_value"]))
        _process("Fonds euro", ff.get_fonds_euro, lambda e: (e["name"], e["id"], e["current_value"]))
        _process("Others", ff.get_other_assets, lambda e: (e["name"], e["id"], e["current_value"]))
        _process(
            "Precious metals",
            ff.get_user_precious_metals,
            lambda e: (e["precious_metal"]["name"], e["id"], e["current_value"]),
            period=False,
        )

        # Investments
        console.log("Fetching investments...")
        node = tree.add("[bold]Investments")
        investments = ff.get_portfolio_investments(session)["result"]
        for account in investments["accounts"]:
            node_account = node.add("[bold]Account: " + account["name"])
            for account in account["securities"]:
                self._match_line(
                    lines_list,
                    node_account,
                    key=account["security"]["name"],
                    id=account["id"],
                    amount=account["current_value"],
                )

        # Cryptos
        console.log("Fetching cryptos...")
        node = tree.add("[bold]Cryptos")
        cryptos = finary_api.user_portfolio.get_portfolio_cryptos(session)["result"]

        for account in cryptos["accounts"]:
            node_account = node.add("[bold]Account: " + account["name"])
            for account in account["cryptos"]:
                self._match_line(
                    lines_list,
                    node_account,
                    key=account["crypto"]["name"],
                    id=account["id"],
                    amount=account["current_value"],
                )

        # Real estate
        console.log("Fetching real estate...")
        node = tree.add("[bold]Real estate")
        real_estate = ff.get_real_estates(session, "1w")["result"]

        for item in real_estate["data"]["real_estates"]:
            self._match_line(lines_list, node, key=item["description"], id=item["id"], amount=item["current_value"])
        for item in real_estate["data"]["scpis"]:
            self._match_line(
                lines_list, node, key=item["scpi"]["name"], id=item["scpi"]["id"], amount=item["current_value"]
            )

        return lines_list, tree

    def _match_line(self, lines_list: List[Dict[str, Any]], node: Tree, key: str, id: str, amount: int) -> None:
        """Internal method used to register a new investment found from Finary."""

        # Discard non-ASCII characters in the key
        key, id, amount = unidecode(key), str(id), round(amount)

        # Add the line to the dictionary of fetched items
        lines_list.append({"key": key, "id": id, "amount": amount})

        # Add the line to the rendering tree
        node_child = node.add(f"{amount} {key} [dim white]{id=}")

        # Fill the line's amount in the portfolio
        for k in [key, id]:
            if self.portfolio.set_child_amount(k, amount):
                return

        # Attach it to root if the line is absent (unless ignored)
        if not self.ignore_orphans:
            node_child.add("[yellow]WARNING: This line did not match with any envelope, attaching to root")
            self.portfolio.add_child(Line(key, amount=amount))

    def _get_cache(self) -> List[Dict[str, Any]]:
        """Attempt to retrieve the cached data. Check if more than an hour has passed since the last update.
        :returns: A key:amount dictionary if the cache file is less than an hour old, None otherwise.
        """

        # Abort retrieving cache if the file doesn't exist
        if not os.path.exists(self.cache_fullpath):
            console.log("No cache file found, fetching data.")
            return []

        # Parse the JSON content
        with open(self.cache_fullpath) as f:
            data = json.load(f)

        # Return the cached content if the cache file is less than the maximum age
        last_updated = datetime.datetime.strptime(data["last_updated"], "%Y-%m-%d %H:%M:%S")
        time_diff = datetime.datetime.now() - last_updated
        hours_passed = int(time_diff.total_seconds() // 3600)

        if hours_passed < self.MAX_CACHE_HOURS:
            console.log(f"Using recently cached data (<{self.MAX_CACHE_HOURS}h max)")
            lines: List[Dict[str, Any]] = data["lines"]
            return lines
        console.log(f"Fetching data (cache file is {hours_passed}h old > {self.MAX_CACHE_HOURS}h max)")
        return []

    def _save_cache(self, lines_list: List[Dict[str, Any]]) -> None:
        """Save the fetched data locally to work offline and reduce the amoutn of calls to the API.
        :param tree: Generated tree object containing all information
        """

        # Save current date and time to a JSON file with the fetched data
        console.log(f"Saving fetched data in '{self.cache_fullpath}'")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {"last_updated": current_time, "lines": lines_list}
        with open(self.cache_fullpath, "w") as f:
            json.dump(data, f, indent=4)
