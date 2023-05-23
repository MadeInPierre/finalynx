"""
```{tip}
This subpackage corresponds to the [portfolio milestone](https://github.com/MadeInPierre/finalynx/milestones?direction=asc&sort=title&state=open) in the development steps.
```

Dedicated subpackage that retrieves your investments from any external source.

Finalynx currently supports Finary as the primary source to obtain real-time portfolio values.
However, any other source might be added in the future by creating a new source option in this
subpackage.
"""
# flake8: noqa
import os
import sys

import finary_uapi.constants  # type: ignore # Set the credentials and cookies constants to a full path

finary_uapi.constants.CREDENTIAL_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")
finary_uapi.constants.COOKIE_FILENAME = os.path.join(os.path.dirname(__file__), "localCookiesMozilla.txt")

from .fetch_finary import FetchFinary
from ..console import console
