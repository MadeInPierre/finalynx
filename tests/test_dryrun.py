import os

import pytest


# Set dummy environment variables for credentials to bypass manual input
@pytest.fixture(autouse=True, scope="session")
def set_credentials_env():
    os.environ["FINARY_EMAIL"] = "test_email"
    os.environ["FINARY_PASSWORD"] = "test_password"
    yield
    os.environ.pop("FINARY_EMAIL")
    os.environ.pop("FINARY_PASSWORD")


# Simply run the demo and pass if there was no error (e.g. missing dependencies)
def test_dryrun() -> None:
    assert os.system("python3 examples/demo.py") == 0
