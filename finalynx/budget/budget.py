from datetime import datetime
from pathlib import Path
from typing import List
from typing import Optional
from typing import TYPE_CHECKING
from typing import Union

import gspread
from rich.prompt import Confirm
from rich.table import Table
from rich.tree import Tree

from ..config import get_active_theme as TH
from ..console import console
from .expense import Constraint
from .expense import Expense
from .expense import Period
from .expense import Status
from .source_n26 import SourceN26

# noreorder
from ._render import _render_expenses_table
from ._review import _i_paid, _payback, _constraint, _period, _comment, _status  # noqa: F401

if TYPE_CHECKING:
    from gspread.worksheet import Worksheet


class Budget:
    MAX_DISPLAY_ROWS = 10

    def __init__(self, service_account_path: Union[str, Path, None] = None) -> None:
        # Google Sheet that serves as the database of expenses, will be connected later
        self._sheet: Optional[Worksheet] = None

        # Initialize the list of expenses, will be fetched later
        self.expenses: List[Expense] = []
        self.n_new_expenses: int = 0
        self.balance: float = 0.0

        # Private copy that only includes expenses that need user review (calculated only once)
        self._pending_expenses: List[Expense] = []

        # Path to the Google Sheets token file, defaults to the OS's default directory
        self._gspread_token_path = (
            Path(service_account_path) if service_account_path else gspread.auth.DEFAULT_SERVICE_ACCOUNT_FILENAME
        )

    def set_gspread_token_path(self, path: Union[str, Path]) -> None:
        """Set the path to the Google Sheets token file, defaults to the OS's default directory."""
        self._gspread_token_path = Path(path)

    def fetch(self, clear_cache: bool, force_signin: bool = False) -> Tree:
        """Get expenses from all sources and return a rich tree to summarize the results.
        This method also updates the google sheets table with the newly found expenses and
        prepares the list of "pending" expenses that need user reviews."""

        # Connect to the Google Sheet that serves as the database of expenses
        with console.status(f"[bold {TH().ACCENT}]Connecting to Google Sheets...", spinner_style=TH().ACCENT):
            try:
                gs = gspread.service_account(filename=self._gspread_token_path)
                sh = gs.open("Finalynx Expenses")
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

        # Initialize the N26 client with the credentials
        if Confirm.ask("Fetch expenses from N26?", default=True):
            source = SourceN26(force_signin)
            tree = source.fetch(clear_cache=bool(clear_cache or force_signin))
            self.balance = source.balance

            # Get the new expenses from the source that are not in the sheet yet
            last_timestamp = max([int(row[0]) for row in sheet_values if str(row[0]).isdigit()])
            new_expenses = list(reversed([e for e in source.get_expenses() if e.timestamp > last_timestamp]))
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
        else:
            tree = Tree("N26 Skipped.")

        # From now on, we will work with the up-to-date list of expenses
        self.expenses = [Expense.from_list(line, i + 2) for i, line in enumerate(sheet_values[1:])]

        # Filter expenses to keep only the ones that are not skipped and incomplete
        self._pending_expenses = [
            t for t in self.expenses if t.status not in [Status.SKIP, Status.DONE, Status.TODO] or t.i_paid is None
        ]

        # Return the tree summary to be displayed in the console
        return tree

    def render_expenses(self) -> Union[Table, str]:
        # Make sure we are already connected to the source and the sheet
        assert self._pending_expenses is not None, "Call `fetch()` first"

        # Display the table of pending expenses
        n_pending = len(self._pending_expenses)

        if n_pending == 0:
            return "[green]No pending expenses 🎉" + (
                f" [dim white]N26 Balance: {self.balance:.2f} €\n" if self.balance > 0.001 else "\n"
            )

        return _render_expenses_table(
            self._pending_expenses[-Budget.MAX_DISPLAY_ROWS :],  # noqa: E203
            title=(
                f"{self.n_new_expenses} new expense{'s' if self.n_new_expenses != 1 else ''} ── {n_pending} need{'s' if n_pending == 1 else ''} review "
                + (f"(displaying {Budget.MAX_DISPLAY_ROWS} first rows)" if n_pending > Budget.MAX_DISPLAY_ROWS else "")
            ),
            caption=f"N26 Balance: {self.balance:.2f} €",
        )

    def render_summary(self) -> Tree:
        """Render a summary of the budget, mainly the current and previous month's totals."""

        # Make sure we are already connected to the source and the sheet
        assert self.expenses is not None, "Call `fetch()` first"
        tree = Tree("Budget", hide_root=True, guide_style=TH().HINT)

        def _get_monthly_expenses(month: int, year: int) -> List[Expense]:
            return [
                e
                for e in self.expenses
                if e.as_datetime().month == month
                and e.as_datetime().year == year
                and e.status != Status.SKIP
                and e.period == Period.MONTHLY
            ]

        def _add_node(title: str, total: float, hint: str = "") -> Tree:
            return tree.add(f"[bold {TH().TEXT}]{title:<11}[/] [{TH().TEXT}]{str(total):>6} € [{TH().ACCENT}]{hint}[/]")

        # Get the yearly total
        now = datetime.now()
        yearly_total = sum(
            [
                (e.i_paid if e.i_paid is not None else 0)
                for e in self.expenses
                if e.as_datetime().year == now.year and e.status != Status.SKIP and e.period == Period.YEARLY
            ]
        )
        _add_node(
            str(now.year),
            round(yearly_total),
            hint=f" {round((yearly_total / 12)):>5} € / month",
        )
        node = tree.add(" ")

        # Get each month's total expenses
        month_totals: List[int] = []
        for i_month in range(1, now.month + 1):
            expenses = _get_monthly_expenses(i_month, now.year)
            monthly_total = round(sum([(e.i_paid if e.i_paid is not None else 0) for e in expenses]))
            month_totals.append(round(monthly_total + (yearly_total / 12)))
            node = _add_node(
                datetime(now.year, i_month, 1).strftime("%B"),
                monthly_total,
                f" {month_totals[-1]:>5} €",
            )

            # Summarize the expenses by category for the last 3 months
            if i_month > now.month - 3:
                for c in [c for c in Constraint if c != Constraint.UNKNOWN]:
                    node.add(
                        f"[{TH().HINT}]{c.value.capitalize():<8} "
                        f"{round(sum([(e.i_paid if e.i_paid is not None else 0) for e in expenses if e.constraint == c])):>5} €"
                    )
                tree.add(" ")

        mean_monthly_total = round(sum(month_totals[:-1]) / len(month_totals[:-1]))
        last_month_name = datetime(now.year, now.month - 1, 1).strftime("%B")

        delta = month_totals[-1] - mean_monthly_total
        tree.add(f"[{TH().TEXT}]Current delta [{'green' if delta > 0 else 'red'}][bold]{delta:>12} €[/]\n")
        tree.add(
            f"[{TH().TEXT}]Mean up to {last_month_name:<9} [{TH().ACCENT}][bold]{mean_monthly_total:>5} €[/] / month"
        )

        return tree

    def interactive_review(self) -> None:
        """Review the list of pending expenses one by one, and update the sheet
        with the new values. This method is interactive, and will clear the
        console between each expense or when the user presses Ctrl+C."""
        assert self._sheet is not None, "Call fetch() first"
        assert self._pending_expenses is not None, "Call `fetch()` first"

        if not self._pending_expenses:
            console.print("[green]You're all done with your expenses! 💸")
            return

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
                    with console.status(f"[bold {TH().ACCENT}]Saving...", spinner_style=TH().ACCENT):
                        self._sheet.update(f"A{t.cell_number}:J{t.cell_number}", [t.to_list()])

            console.clear()
            console.print("[bold]All done![/] 🎉")
        except KeyboardInterrupt:
            console.clear()

    def _fetch_sheet_values(self) -> List[List[str]]:
        """Get the latest values from the Google Sheet."""
        assert self._sheet is not None, "Call connect() first"
        with console.status(
            f"[bold {TH().ACCENT}]Fetching previous expenses from Google Sheets...",
            spinner_style=TH().ACCENT,
        ):
            return self._sheet.get_all_values()  # type: ignore
