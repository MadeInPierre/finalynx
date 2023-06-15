from typing import List
from typing import Optional

import gspread
from rich.table import Table

from ..console import console
from .expense import Expense
from .expense import Status
from .source_n26 import SourceN26

# noreorder
from ._render import _render_expenses_table
from ._review import _i_paid, _payback, _constraint, _period, _comment, _status  # noqa: F401


class Budget:
    MAX_DISPLAY_ROWS = 20

    def __init__(self) -> None:
        # Initialize the N26 client with the credentials, no connection yet
        self._source: Optional[SourceN26] = None

        # Google Sheet that serves as the database of expenses, will be connected later
        self._sheet = None

        # # Initialize the list of expenses, will be fetched later
        self.expenses: List[Expense] = []
        self._new_expenses: List[Expense] = []  # Freshly fetched from the source
        self._pending_expenses: List[Expense] = []  # Filtered to keep only the ones that need review
        self.balance: float = 0.0

    def fetch(self, email: str, password: str, device_token: str) -> List[Expense]:
        """TODO"""

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

        # Make sure we are already connected to the source and the sheet
        assert self._source is not None, "Something went wrong with the connection to N26"
        assert self._sheet is not None, "Something went wrong with the connection to GSheets"

        # Fetch the latest values from the source and the sheet
        self.balance = self._fetch_source_balance()
        expenses = self._fetch_source_expenses()
        sheet_values = self._fetch_sheet_values()

        # Get the new expenses from the source that are not in the sheet yet
        last_row_timestamp = int(sheet_values[-1][0]) if str(sheet_values[-1][0]).isdigit() else 0
        self._new_expenses = [e for e in expenses if e.timestamp > last_row_timestamp]

        # Add the new expenses to the sheet
        if len(self._new_expenses) > 0:
            first_empty_row = len(sheet_values) + 1

            self._sheet.update(
                f"A{first_empty_row}:D{first_empty_row + len(self._new_expenses)}",
                [d.to_list()[:4] for d in self._new_expenses],
            )

        # Fetch the latest values from the sheet again to get the complete list of expenses
        sheet_values = self._fetch_sheet_values()  # TODO improve

        # From now on, we will work with the up-to-date list of expenses
        self.expenses = [Expense.from_list(line, i + 2) for i, line in enumerate(sheet_values[1:])]

        # Filter expenses to keep only the ones that are not skipped and incomplete
        self._pending_expenses = [
            t for t in self.expenses if t.status not in [Status.SKIP, Status.DONE] or t.i_paid is None
        ]

        # Return the list for user convenience
        return self.expenses

    def render_expenses(self) -> Table:
        # Make sure we are already connected to the source and the sheet
        assert self._new_expenses is not None, "Call `fetch()` first"
        assert self._pending_expenses is not None, "Call `fetch()` first"

        # Display the table of pending expenses
        n_new, n_pending = len(self._new_expenses), len(self._pending_expenses)
        return _render_expenses_table(
            self._pending_expenses[-Budget.MAX_DISPLAY_ROWS :],  # noqa: E203
            title=(
                f"{n_new} new expense{'s' if n_new != 1 else ''} ── {n_pending} need{'s' if n_pending == 1 else ''} review "
                + (f"(displaying {Budget.MAX_DISPLAY_ROWS} first rows)" if n_pending > Budget.MAX_DISPLAY_ROWS else "")
            ),
            caption=f"N26 Balance: {self.balance:.2f} €",
        )

    def interactive_review(self) -> None:
        """Review the list of pending expenses one by one, and update the sheet
        with the new values. This method is interactive, and will clear the
        console between each expense or when the user presses Ctrl+C."""
        assert self._sheet is not None, "Call fetch() first"
        assert self._pending_expenses, "Call fetch() first"

        # Make space so that the main table is not hidden by the next console clears
        console.print("\n" * console.height)
        console.clear()

        # Review pending expenses in reverse (most recent first) for convenience
        review_expenses = self._pending_expenses[::-1]

        # For each expense, ask the user to set each field to classify the expense
        try:
            for i, t in enumerate(review_expenses):
                _skip_line = False

                for method in [
                    _i_paid,
                    _payback,
                    _constraint,
                    _period,
                    _comment,
                    _status,
                ]:
                    result = method(review_expenses, i)
                    if result is None:
                        console.clear()
                        return
                    elif result is False:
                        _skip_line = True
                        break

                if not _skip_line:
                    with console.status("[bold green]Saving..."):
                        self._sheet.update(f"A{t.cell_number}:J{t.cell_number}", [t.to_list()])

            console.clear()
            console.print("[bold]All done![/] 🎉")
        except KeyboardInterrupt:
            console.clear()

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
