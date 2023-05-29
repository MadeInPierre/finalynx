import json
import re

import requests
from rich.tree import Tree

from .source_base import SourceBase

# Todo integrate user specific data into credentials.json file
MyRealT_Wallet_Address = "0x10df7DD932E655c01CC7A35eC23711B1d4153882"

Gnosis_API_TokenList_URI = "https://blockscout.com/xdai/mainnet/api?module=account&action=tokenlist&address="
RealT_API_TokenList_URI = "https://api.realt.community/v1/token"


class SourceRealT(SourceBase):
    # No spaces, alphanumeric name only
    SOURCE_NAME = "RealT"

    def __init__(self, clear_cache: bool = False, ignore_orphans: bool = False) -> None:
        """Write a description of how your source works here, with a list of what each
        argument does:
        :param clear_cache: Forces to clear the last fetch's saved results.
        :param ignore_orphans: Don't create new lines at the root of the portfolio if some
        investments have been fetched but have not been matched with any existing node.
        """
        super().__init__(self.SOURCE_NAME, clear_cache, ignore_orphans)

    def _fetch_data(self, tree: Tree) -> None:
        """Use this method to fetch your data however you want! CSV, PDF, API, manual input...
        Use any logic you want here! Just use this method once you have fetched an investment:
        """

        # Todo optimize API call with API key and/or cached file
        # Get list of all Realtoken info needed from RealT
        realt_tokenlist = json.loads(requests.get(RealT_API_TokenList_URI).text)
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
        gnosis_tokenlist = json.loads(requests.get(Gnosis_API_TokenList_URI + MyRealT_Wallet_Address).text)

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
