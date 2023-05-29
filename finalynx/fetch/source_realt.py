import json
import re

import requests
from rich.tree import Tree

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
        """Use this method to fetch your data however you want! CSV, PDF, API, manual input...
        Use any logic you want here! Just use this method once you have fetched an investment:
        """

        with console.status(f"[bold green]Fetching data from {self.name}..."):
            # Todo optimize API call with API key and/or cached file
            # Get list of all Realtoken info needed from RealT
            realt_tokenlist = json.loads(requests.get(REALT_API_TOKENLIST_URI).text)
            realt_tokeninfo = {}
            for item in realt_tokenlist:
                realt_tokeninfo.update(
                    {
                        item.get("symbol").lower(): {
                            "fullName": item.get("fullName"),
                            "shortName": item.get("shortName"),
                            "tokenPrice": item.get("tokenPrice"),
                            "currency": item.get("currency"),
                            "uuid": item.get("uuid"),
                        }
                    }
                )

            # Get list of token own from Gnosis address
            # TODO integrate user specific data into credentials.json file
            gnosis_tokenlist = json.loads(requests.get(GNOSIS_API_TOKENLIST_URI + self.wallet_address).text)

        # Display the lines found to the console, you can create a nested tree if you want
        node = tree.add("RealT")

        # Register the real investment information, will be cached and matched to the portfolio
        for item in gnosis_tokenlist.get("result"):
            if re.match(r"^REALTOKEN", str(item.get("symbol"))):
                self._register_fetchline(
                    tree_node=node,  # this line will display under the category, use `tree` for root
                    name=realt_tokeninfo[str(item.get("symbol")).lower()]["shortName"],
                    id=realt_tokeninfo[str(item.get("symbol")).lower()]["uuid"],
                    account="My RealT Portfolio",
                    amount=(float(item.get("balance")) / pow(10, int(item.get("decimals"))))
                    * realt_tokeninfo[str(item.get("symbol")).lower()]["tokenPrice"],
                    currency=realt_tokeninfo[str(item.get("symbol")).lower()]["currency"],
                )
            if re.match(r"^armmR", str(item.get("symbol"))):
                self._register_fetchline(
                    tree_node=node,  # this line will display under the category, use `tree` for root
                    name=realt_tokeninfo[re.sub(r"armm", "", str(item.get("symbol"))).lower()]["shortName"],
                    id=realt_tokeninfo[re.sub(r"armm", "", str(item.get("symbol"))).lower()]["uuid"],
                    account="My RealT Portfolio",
                    amount=(float(item.get("balance")) / pow(10, int(item.get("decimals"))))
                    * realt_tokeninfo[re.sub(r"armm", "", str(item.get("symbol"))).lower()]["tokenPrice"],
                    currency=realt_tokeninfo[re.sub(r"armm", "", str(item.get("symbol"))).lower()]["currency"],
                )
