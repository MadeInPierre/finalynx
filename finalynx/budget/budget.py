from typing import List
from typing import Optional
from typing import TYPE_CHECKING

import gspread
from rich.table import Table
from rich.tree import Tree

from ..console import console
from .expense import Expense
from .expense import Status
from .source_n26 import SourceN26

# noreorder
from ._render import _render_expenses_table
from ._review import _i_paid, _payback, _constraint, _period, _comment, _status  # noqa: F401

if TYPE_CHECKING:
    from gspread.worksheet import Worksheet


class Budget:
    MAX_DISPLAY_ROWS = 20

    def __init__(self) -> None:
        # Google Sheet that serves as the database of expenses, will be connected later
        self._sheet: Optional[Worksheet] = None

        # Initialize the list of expenses, will be fetched later
        self.expenses: List[Expense] = []
        self.n_new_expenses: int = -1
        self.balance: float = 0.0

        # Private copy that only includes expenses that need user review (calculated only once)
        self._pending_expenses: List[Expense] = []

    def fetch(self, email: str, password: str, device_token: str, clear_cache: bool) -> Tree:
        """Get expenses from all sources and return a rich tree to summarize the results.
        This method also updates the google sheets table with the newly found expenses and
        prepares the list of "pending" expenses that need user reviews."""

        # Initialize the N26 client with the credentials
        with console.status("[bold green]Fetching from N26...[/] [dim white](you may have to confirm in the app)"):
            source = SourceN26(email, password, device_token)
            tree = source.fetch(clear_cache)
            self.balance = source.balance

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
        assert self._sheet is not None, "Something went wrong with the connection to GSheets"

        # Fetch the latest values from the the sheet
        sheet_values = self._sheet.get_all_values()

        # Get the new expenses from the source that are not in the sheet yet
        sheet_timestamps = [int(row[0]) for row in sheet_values if str(row[0]).isdigit()]
        new_expenses = list(reversed([e for e in source.get_expenses() if e.timestamp not in sheet_timestamps]))
        self.n_new_expenses = len(new_expenses)

        # Add the new expenses to the sheet
        if self.n_new_expenses > 0:
            first_empty_row = len(sheet_values) + 1

            self._sheet.update(
                f"A{first_empty_row}:D{first_empty_row + len(new_expenses)}",
                [d.to_list()[:4] for d in new_expenses],
            )

        # Fetch the latest values from the sheet again to get the complete list of expenses
        sheet_values = self._fetch_sheet_values()  # TODO improve

        # From now on, we will work with the up-to-date list of expenses
        self.expenses = [Expense.from_list(line, i + 2) for i, line in enumerate(sheet_values[1:])]

        # Filter expenses to keep only the ones that are not skipped and incomplete
        self._pending_expenses = [
            t for t in self.expenses if t.status not in [Status.SKIP, Status.DONE] or t.i_paid is None
        ]

        # Return the tree summary to be displayed in the console
        return tree

    def render_expenses(self) -> Table:
        # Make sure we are already connected to the source and the sheet
        assert self.n_new_expenses > -1, "Call `fetch()` first"
        assert self._pending_expenses is not None, "Call `fetch()` first"

        # Display the table of pending expenses
        n_pending = len(self._pending_expenses)
        return _render_expenses_table(
            self._pending_expenses[-Budget.MAX_DISPLAY_ROWS :],  # noqa: E203
            title=(
                f"{self.n_new_expenses} new expense{'s' if self.n_new_expenses != 1 else ''} ── {n_pending} need{'s' if n_pending == 1 else ''} review "
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

    def _fetch_sheet_values(self) -> List[List[str]]:
        """Get the latest values from the Google Sheet."""
        assert self._sheet is not None, "Call connect() first"
        with console.status("[bold green]Fetching previous expenses from Google Sheets..."):
            return self._sheet.get_all_values()  # type: ignore
