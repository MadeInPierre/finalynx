from dataclasses import dataclass
from typing import Optional


@dataclass
class FetchKey:  # TODO
    name: Optional[str] = None
    id: Optional[str] = None
    account: Optional[str] = None

    def match(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        account: Optional[str] = None,
    ) -> bool:
        if not name and not id and not account:
            raise ValueError("FetchKey instance must have at least one field set.")
        return self.name == name or self.id == id or self.account == account
