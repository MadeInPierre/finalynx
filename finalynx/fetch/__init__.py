# flake8: noqa
import os
import sys

import finary_api.constants  # type: ignore # Set the credentials and cookies constants to a full path

finary_api.constants.CREDENTIAL_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")
finary_api.constants.COOKIE_FILENAME = os.path.join(os.path.dirname(__file__), "localCookiesMozilla.txt")

from .finary_fetch import finary_fetch
from ..console import console
