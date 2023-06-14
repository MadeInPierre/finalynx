from typing import List
from typing import Optional

import gspread

from ..console import console
from .expense import Expense
from .expense import Status
from .render_table import generate_table
from .source_n26 import SourceN26


class Budget:
    MAX_DISPLAY_ROWS = 20

    def __init__(self) -> None:
        # Initialize the N26 client with the credentials, no connection yet
        self._source: Optional[SourceN26] = None

        # Google Sheet that serves as the database of expenses, will be connected later
        self._sheet = None

        # # Initialize the list of expenses and the account balance, will be fetched later
        self._all_expenses: List[Expense] = []
        # self._source_balance: float = 0.0

    def connect(self, email: str, password: str, device_token: str) -> None:
        # Initialize the N26 client with the credentials
        with console.status("[bold green]Connecting to N26...[/] [dim white](you may have to confirm in the app)"):
            self._source = SourceN26(email, password, device_token)

        # Connect to the Google Sheet that serves as the database of expenses
        with console.status("[bold green]Connecting to Google Sheets..."):
            try:
                gs = gspread.service_account()
                sh = gs.open("N26 Expenses")
                self._sheet = sh.worksheet("Sheet1")
            except Exception as e:  # noqa
                console.log(
                    "[red][bold]Error:[/] Couldn't connect to GSheets, have you placed your "
                    "personal service_account.json token file in your OS's default directory?"
                )

    def run(self) -> None:
        """Run the budgeting process."""
        # Make sure we are already connected to the source and the sheet
        assert self._sheet is not None, "Call connect() first"
        assert self._source is not None, "Call connect() first"

        # Fetch the latest values from the source and the sheet
        balance = self._fetch_source_balance()
        expenses = self._fetch_source_expenses()
        sheet_values = self._fetch_sheet_values()

        # Get the new expenses from the source that are not in the sheet yet
        last_row_timestamp = int(sheet_values[-1][0]) if str(sheet_values[-1][0]).isdigit() else 0
        new_expenses = [e for e in expenses if e.timestamp > last_row_timestamp]

        # Add the new expenses to the sheet
        if len(new_expenses) > 0:
            first_empty_row = len(sheet_values) + 1

            self._sheet.update(
                f"A{first_empty_row}:D{first_empty_row + len(new_expenses)}", [d.to_list()[:4] for d in new_expenses]
            )

        # Fetch the latest values from the sheet again to get the complete list of expenses
        sheet_values = self._fetch_sheet_values()  # TODO improve

        # From now on, we will work with the up-to-date list of expenses
        updated_expenses = [Expense.from_list(line, i + 2) for i, line in enumerate(sheet_values[1:])]

        # Filter expenses to keep only the ones that are not skipped and incomplete
        pending_expenses = [
            t for t in updated_expenses if t.status not in [Status.SKIP, Status.DONE] or t.i_paid is None
        ]

        # Display the table of pending expenses
        n_new, n_pending = len(new_expenses), len(pending_expenses)
        table = generate_table(
            pending_expenses[-Budget.MAX_DISPLAY_ROWS :],  # noqa: E203
            title=(
                f"{n_new} new expense{'s' if n_new != 1 else ''} ── {n_pending} need{'s' if n_pending == 1 else ''} review "
                + (f"(displaying {Budget.MAX_DISPLAY_ROWS} first rows)" if n_pending > Budget.MAX_DISPLAY_ROWS else "")
            ),
            caption=f"N26 Balance: {balance:.2f} €",
        )
        console.print("\n\n\n", table, "\n\n\n", sep="\n")

    def _fetch_source_balance(self) -> float:
        """Get the account balance from the source."""
        assert self._source is not None, "Call connect() first"
        with console.status("[bold green]Fetching N26 balance..."):
            return self._source.fetch_balance()

    def _fetch_source_expenses(self) -> List[Expense]:
        """Get the list of expenses from the source."""
        assert self._source is not None, "Call connect() first"
        with console.status("[bold green]Fetching N26 expenses..."):
            return self._source.fetch_expenses()

    def _fetch_sheet_values(self) -> List[List[str]]:
        """Get the latest values from the Google Sheet."""
        assert self._sheet is not None, "Call connect() first"
        with console.status("[bold green]Fetching previous expenses from Google Sheets..."):
            return self._sheet.get_all_values()
