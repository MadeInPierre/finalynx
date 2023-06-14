from typing import List

import iso18245
from n26.api import Api
from n26.config import Config

from .expense import Expense


# TODO Harmonize credentials with SourceBase (env vars, etc.)


class SourceN26:
    """Fetch expenses from N26"""

    def __init__(self, email: str, password: str, device_token: str) -> None:
        """Initialize the N26 client with the credentials."""
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

    def fetch_balance(self) -> float:
        """Get the account balance."""
        n26_balance = self._client.get_balance()
        return float(n26_balance["availableBalance"])

    def fetch_expenses(self, limit: int = 20) -> List[Expense]:
        """Get the list of expenses."""
        response = self._client.get_transactions(limit=limit)

        # Transform the list of expenses into a list of Expense objects
        expenses: List[Expense] = []
        for t in response:
            # Transform the MCC into a human-readable description
            try:
                merchant_category = iso18245.get_mcc(str(t["mcc"])).iso_description
            except Exception:
                merchant_category = "---"

            # If there is no merchant name, it means it's an internal transfer
            merchant_name = t["merchantName"] if "merchantName" in t else "(transfer)"

            # Create the Expense object
            expenses.append(
                Expense(
                    int(t["createdTS"]),
                    float(t["amount"]),
                    merchant_name,
                    merchant_category,
                )
            )

        return expenses
