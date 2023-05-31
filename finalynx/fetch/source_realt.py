import json
import re

import requests
from rich.tree import Tree

from ..config import get_active_theme as TH
from ..console import console
from .source_base import SourceBase


GNOSIS_API_TOKENLIST_URI = "https://blockscout.com/xdai/mainnet/api?module=account&action=tokenlist&address="
REALT_API_TOKENLIST_URI = "https://api.realt.community/v1/token"


class SourceRealT(SourceBase):
    def __init__(
        self,
        wallet_address: str,
        name: str = "RealT",
    ) -> None:
        """RealT wrapper to fetch an address' investments.
        :param wallet_address: Your wallet address.
        :param name: Set this source's name, can be changed when using multiple RealT sources
        for multiple RealT addresses.
        :param clear_cache: Forces to clear the last fetch's saved results.
        :param ignore_orphans: Don't create new lines at the root of the portfolio if some
        investments have been fetched but have not been matched with any existing node.
        """
        super().__init__(name)
        self.wallet_address = wallet_address

    def _fetch_data(self, tree: Tree) -> None:
        """Get investments from RealT and match them with information found on the specified wallet."""

        with console.status(f"[bold {TH().ACCENT}]Fetching data from {self.name}...", spinner_style=TH().ACCENT):
            # Todo optimize API call with API key and/or cached file
            # Get list of all Realtoken info needed from RealT
            realt_tokenlist = json.loads(requests.get(REALT_API_TOKENLIST_URI).text)
            realt_tokeninfo = {}
            for item in realt_tokenlist:
                realt_tokeninfo.update(
                    {
                        item["uuid"].lower(): {
                            "fullName": item["fullName"],
                            "shortName": item["shortName"],
                            "tokenPrice": item["tokenPrice"],
                            "uuid": item["uuid"],
                        }
                    }
                )

            # Get list of token own from Gnosis address
            gnosis_tokenlist = json.loads(requests.get(GNOSIS_API_TOKENLIST_URI + self.wallet_address).text)

            # Display the lines found to the console, you can create a nested tree if you want
            node = tree.add("RealT")

            # Register the real investment information, will be cached and matched to the portfolio
            for item in gnosis_tokenlist["result"]:
                address = str(item["contractAddress"])
                try:
                    amount = float(item["balance"]) / pow(10, int(item["decimals"]))

                    if re.match(r"^REALTOKEN", str(item["symbol"])):
                        info = realt_tokeninfo[address.lower()]

                        self._register_fetchline(
                            tree_node=node,
                            name=info["shortName"],
                            id=info["uuid"],
                            account=self.name,
                            amount=amount * info["tokenPrice"],
                            currency="$",
                        )

                    if re.match(r"^armmR", str(item["symbol"])):
                        original_contract_address = json.loads(requests.get(GNOSIS_API_TOKENLIST_URI + address).text)
                        key = str(original_contract_address["result"][0]["contractAddress"]).lower()

                        self._register_fetchline(
                            tree_node=node,
                            name=realt_tokeninfo[key]["shortName"],
                            id=realt_tokeninfo[key]["uuid"],
                            account=self.name,
                            amount=amount * realt_tokeninfo[key]["tokenPrice"],
                            currency="$",
                        )

                except Exception as e:
                    self._log(f"[yellow][bold]Warning:[/] failed to parse line '{address}', skipping ({e})")
