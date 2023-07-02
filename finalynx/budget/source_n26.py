import iso18245
from n26.api import Api
from n26.config import Config
from rich.tree import Tree

from ..config import get_active_theme as TH
from .source_base_expense import SourceBaseExpense


# TODO Harmonize credentials with SourceBase (env vars, etc.)


class SourceN26(SourceBaseExpense):
    """Fetch expenses from N26"""

    def __init__(
        self,
        email: str,
        password: str,
        device_token: str,
        fetch_limit: int = 100,
        cache_validity: int = 12,
    ) -> None:
        """Initialize the N26 client with the credentials."""
        super().__init__("N26", cache_validity)
        self.fetch_limit = fetch_limit

        # Create config object with info from file
        conf = Config(validate=False)
        conf.USERNAME.value = email
        conf.PASSWORD.value = password
        conf.DEVICE_TOKEN.value = device_token
        conf.LOGIN_DATA_STORE_PATH.value = "~/.config/n26/token_data"
        conf.MFA_TYPE.value = "app"
        conf.validate()

        # Get the account balance and list of expenses
        self._client = Api(conf)

        # Give access to the account balance, will be set later
        self.balance: float = 0.0

    def _fetch_data(self, tree: Tree) -> None:
        """Abstract method, must be averridden by children classes. This method retrieves the data
        from the source, and calls `_register_fetchline` to create a `FetchLine` instance representing
        each fetched investment."""

        # Fetch the account balance
        self.balance = float(self._client.get_balance()["availableBalance"])

        """Get the list of expenses."""
        response = self._client.get_transactions(limit=self.fetch_limit)

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
