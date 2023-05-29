import os

import pytest
from finalynx import Assistant
from finalynx import Portfolio


# Set dummy environment variables for credentials to bypass manual input
@pytest.fixture(autouse=True, scope="session")
def set_credentials_env():
    if not os.environ.get("FINARY_EMAIL"):
        os.environ["FINARY_EMAIL"] = "test_email"
    if not os.environ.get("FINARY_PASSWORD"):
        os.environ["FINARY_PASSWORD"] = "test_password"

    print(f"Using email '{os.environ.get('FINARY_EMAIL')}'")
    yield

    if os.environ.get("FINARY_EMAIL"):
        os.environ.pop("FINARY_EMAIL")
    if os.environ.get("FINARY_PASSWORD"):
        os.environ.pop("FINARY_PASSWORD")


def test_demo_account(n_investments: int = 24) -> None:
    """Log in to the demo Finary account (credentials saved in
    CI/CD secrets) and make sure everything was found."""
    portfolio = Portfolio()
    Assistant(portfolio, ignore_argv=True, show_data=True, force_signin=True).run()
    assert len(portfolio.children) == n_investments, f"Must get {n_investments} investments from Finary demo account."


def test_session() -> None:
    """Uses cookies saved from the previous run to fetch again"""
    assert os.system("python3 examples/demo.py -c") == 0


def test_cache() -> None:
    """Uses data cached from the previous run (no need to fetch)"""
    assert os.system("python3 examples/demo.py") == 0
