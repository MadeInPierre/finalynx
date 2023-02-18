import os
import sys

# Set the credentials and cookies constants to a full path
import finary_api.constants

current_path = os.path.dirname(__file__)
finary_api.constants.CREDENTIAL_FILE = os.path.join(current_path, "credentials.json")
finary_api.constants.COOKIE_FILENAME = os.path.join(
    current_path, "localCookiesMozilla.txt"
)

from .finary_fetch import finary_fetch
from ..console import console
