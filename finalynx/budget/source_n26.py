import json
import os
import uuid
from typing import Optional

import iso18245
from n26.api import Api
from n26.config import Config
from rich.prompt import Confirm
from rich.tree import Tree

from ..config import get_active_theme as TH
from ..console import console
from .source_base_expense import SourceBaseExpense


class SourceN26(SourceBaseExpense):
    """Fetch expenses from N26"""

    def __init__(
        self,
        force_signin: bool = False,
        fetch_limit: int = 100,
        cache_validity: int = 12,
    ) -> None:
        """Initialize the N26 client with the credentials."""
        super().__init__("N26", cache_validity)
        self.force_signin = force_signin
        self.fetch_limit = fetch_limit

        # Create config object with info from file
        self.CREDENTIAL_FILE = os.path.join(os.path.dirname(__file__), "n26_credentials.json")

        # Give access to the account balance, will be set later
        self.balance: float = 0.0

    def _authenticate(self) -> Optional[Config]:
        """Internal method used to signin and retrieve a session from Finary.
        Called by `_fetch_data` once, only exists for better logic separation.
        :returns: A session for fetching data if everything worked, None otherwise.
        """

        # Let the user reset its credentials
        if self.force_signin:
            if os.path.exists(self.CREDENTIAL_FILE):
                if not Confirm.ask("Reuse saved credentials? Otherwise, they will also be deleted.", default=True):
                    os.remove(self.CREDENTIAL_FILE)

        # Skip credential input if it was already set in environment variables
        if os.environ.get("N26_EMAIL") and os.environ.get("N26_PASSWORD") and os.environ.get("N26_DEVICE_TOKEN"):
            self._log("Found N26 credentials in environment variables, logging in.")

        # Otherwise, ask for manual input if credentials are missing
        else:
            credentials = {}
            if os.path.exists(self.CREDENTIAL_FILE):
                self._log("Found saved credentials, logging in.")

                cred_file = open(self.CREDENTIAL_FILE)
                credentials = json.load(cred_file)
            else:
                self._log("Credentials in environment variables not set, asking for manual input.")

                credentials["email"] = console.input("Enter your N26 [yellow bold]email[/]: ")
                credentials["password"] = console.input("Enter your N26 [yellow bold]password[/]: ", password=True)
                credentials["device_token"] = console.input("Enter your device token: ")

                if not credentials["device_token"]:
                    credentials["device_token"] = str(uuid.uuid1())

                if Confirm.ask(
                    f"Would like to save your credentials in [green]'{self.CREDENTIAL_FILE}'[/]?",
                    default=False,
                    show_default=True,
                ):
                    with open(self.CREDENTIAL_FILE, "w") as f:
                        f.write(json.dumps(credentials, indent=4))

            os.environ["N26_EMAIL"] = credentials["email"]
            os.environ["N26_PASSWORD"] = credentials["password"]
            os.environ["N26_DEVICE_TOKEN"] = credentials["device_token"]

        # Create the N26 config with the info now available as environment variables
        if not (os.environ.get("N26_EMAIL") and os.environ.get("N26_PASSWORD") and os.environ.get("N26_DEVICE_TOKEN")):
            self._log("[bold red]No credentials or environment variables set. Skipping fetching.[/]")
            return None

        conf = Config(validate=False)
        conf.USERNAME.value = os.environ.get("N26_EMAIL")
        conf.PASSWORD.value = os.environ.get("N26_PASSWORD")
        conf.DEVICE_TOKEN.value = os.environ.get("N26_DEVICE_TOKEN")
        conf.LOGIN_DATA_STORE_PATH.value = "~/.config/n26/token_data"
        conf.MFA_TYPE.value = "app"
        conf.validate()

        # Delete login variables just in case
        if os.environ.get("N26_EMAIL"):
            os.environ.pop("N26_EMAIL")
        if os.environ.get("N26_PASSWORD"):
            os.environ.pop("N26_PASSWORD")
        if os.environ.get("N26_DEVICE_TOKEN"):
            os.environ.pop("N26_DEVICE_TOKEN")

        return conf

    def _fetch_data(self, tree: Tree) -> None:
        """Abstract method, must be averridden by children classes. This method retrieves the data
        from the source, and calls `_register_fetchline` to create a `FetchLine` instance representing
        each fetched investment."""

        # Get the account balance and list of expenses
        conf = self._authenticate()
        if conf is None:
            raise ValueError("Could not setup N26 login info.")
        _client = Api(conf)

        # Fetch the data
        with console.status(
            f"[bold {TH().ACCENT}]Fetching from N26...[/] [dim white](you may have to confirm in the app)",
            spinner_style=TH().ACCENT,
        ):
            # Fetch the account balance
            self.balance = float(_client.get_balance()["availableBalance"])

            # Get the list of expenses.
            response = _client.get_transactions(limit=self.fetch_limit)

        # Transform the list of expenses into a list of Expense objects
        for t in response:
            # Transform the MCC into a human-readable description
            try:
                merchant_category = iso18245.get_mcc(str(t["mcc"])).iso_description
            except Exception:
                merchant_category = "---"

            # If there is no merchant name, it means it's an internal transfer
            if "merchantName" in t:
                merchant_name = t["merchantName"]
            else:
                merchant_name = t["referenceText"] if "referenceText" in t else ""
                merchant_name += (" with " + t["partnerName"]) if "partnerName" in t else ""

            # Create the Expense object
            self._register_expense(
                int(t["confirmed"]),
                float(t["amount"]),
                "€",
                merchant_name,
                merchant_category,
            )

        # Add a summary of what has been fetched to the data tree
        tree.add(f"{len(self._fetched_items)} expense(s) found [{TH().HINT}](limited to {self.fetch_limit})")
