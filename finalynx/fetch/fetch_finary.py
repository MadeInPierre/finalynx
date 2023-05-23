import datetime
import json
import os
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import finary_uapi.__main__ as ff
import finary_uapi.constants
import finary_uapi.user_portfolio
from finalynx.fetch.fetch_line import FetchLine
from requests import Session
from rich.prompt import Confirm
from rich.tree import Tree
from unidecode import unidecode

from ..console import console
from ..portfolio.folder import Portfolio
from ..portfolio.line import Line
from .fetch import Fetch


class FetchFinary(Fetch):  # TODO update docstrings
    """Wrapper class for the `finary_uapi` package."""

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
        `finary_uapi` to refresh your session (to be confirmed). However, this is not recommended since only storing
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
            console.log("Deleting cache per user request.")
            os.remove(self.cache_fullpath)

        # This will hold a key:amount dictionary of all lines found in the Finary account
        fetched_lines: List[FetchLine] = self._get_cache()  # try to get the data in the cache first
        tree = Tree("Finary API", highlight=True, hide_root=True)

        # If there's no valid cache, signin and fetch the data online
        if not fetched_lines:
            session = self._authenticate()
            if not session:
                return Tree("Finary signin failed.")

            try:
                fetched_lines = self._fetch_data(session, tree)
            except Exception as e:
                console.log("[red bold]Error: Couldn't fetch data, please try using the `-f` option to signin again.")
                console.log(f"[red][bold]Details:[/] {e}")
                return tree

            # Save what has been found in a cache file for offline use and better performance at next launch
            self._save_cache(fetched_lines)

        # If the cache is not empty, Match all lines to the portfolio hierarchy
        for fline in fetched_lines:
            name = fline.name if fline.name else "Unknown"
            matched_lines: List[Line] = list(set(self.portfolio.match_lines(fline)))  # merge identical instances

            # Set attributes to the first matched line
            if matched_lines:
                # Issue a warning if multiple lines matched, try to set a stricter key
                if len(matched_lines) > 1:
                    console.log(
                        f"[yellow][bold]Warning:[/] Line '{name}' matched with multiple nodes, updating first only."
                    )

                # Update the first line's attributes based on whata has been found online
                fline.update_line(matched_lines[0])

            # If no line matched, attach a fake line to root (unless ignored)
            elif not self.ignore_orphans:
                console.log(
                    f"[yellow][bold]Warning:[/] Line '{name}' did not match with any portfolio node, attaching to root."
                )
                self.portfolio.add_child(Line(name, amount=fline.amount))

        # Return a rich tree to be displayed in the console as a recap of what has been fetched
        console.log("Done fetching Finary data.")
        return tree

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

    def _fetch_data(self, session: Session, tree: Tree) -> List[FetchLine]:
        """Internal method used to fetch every investment in your Finary account.
        :returns: A dictionary of all fetched investments (name:amount format), and a `Tree`
        instance which can be displayed in the console to make sure everything was retrieved.
        """

        # Create a rich Tree to display the fetched data nicely
        fetched_lines: List[FetchLine] = []

        # Simple utility function
        def start_step(step_name: str, tree_node: Tree) -> Tree:
            console.log(f"Fetching {step_name.lower()}...")
            return tree_node.add(f"[bold]{step_name}")

        # Checkings
        node = start_step("Checkings", tree)
        for e in ff.get_checking_accounts(session, "1w")["result"]["data"]:
            self._register_fetchline(
                fetched_lines=fetched_lines,
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
                fetched_lines=fetched_lines,
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
                fetched_lines=fetched_lines,
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
                fetched_lines=fetched_lines,
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
                fetched_lines=fetched_lines,
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
                    fetched_lines=fetched_lines,
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
                    fetched_lines=fetched_lines,
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
                fetched_lines=fetched_lines,
                tree_node=node,
                name=e["description"],
                id=e["id"],
                account=e["account"]["name"],
                amount=e["display_current_value"],
                currency=e["account"]["display_currency"]["symbol"],
            )
        for e in real_estate["scpis"]:
            self._register_fetchline(
                fetched_lines=fetched_lines,
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
                fetched_lines=fetched_lines,
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
                fetched_lines=fetched_lines,
                tree_node=node,
                name=e["name"],
                id=e["id"],
                account=e["name"],
                amount=-e["display_balance"],
                currency=e["display_currency"]["symbol"],
            )

        return fetched_lines

    def _register_fetchline(
        self,
        fetched_lines: List[FetchLine],
        tree_node: Tree,
        name: str,
        id: str,
        account: str,
        amount: int,
        currency: str,
        custom: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Internal method used to register a new investment found from Finary."""

        # Skip malformed lines (or lines with 0 euros invested)
        if not (name or id or account) or amount < 1.0:
            return

        # Discard non-ASCII characters in the fields
        name, id, account, amount = unidecode(name), str(id), unidecode(account), round(float(amount))

        # Add the line to the rendering tree
        tree_node.add(f"{amount} {currency} {name} [dim white]{id=} {account=}")

        # Form a FetLine instance from the information given and return it
        fetched_lines.append(
            FetchLine(name=name, id=id, account=account, custom=custom, amount=amount, currency=currency)
        )

    def _get_cache(self) -> List[FetchLine]:
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
            return [FetchLine.from_dict(line_dict) for line_dict in data["lines"]]
        console.log(f"Fetching data (cache file is {hours_passed}h old > {self.MAX_CACHE_HOURS}h max)")
        return []

    def _save_cache(self, fetched_lines: List[FetchLine]) -> None:
        """Save the fetched data locally to work offline and reduce the amoutn of calls to the API.
        :param tree: Generated tree object containing all information
        """

        # Save current date and time to a JSON file with the fetched data
        console.log(f"Saving fetched data in '{self.cache_fullpath}'")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {"last_updated": current_time, "lines": [line.to_dict() for line in fetched_lines]}
        with open(self.cache_fullpath, "w") as f:
            json.dump(data, f, indent=4)
