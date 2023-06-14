from datetime import datetime
from typing import List
from typing import Optional

import gspread
import pytz
from rich import box
from rich.table import Table

from ..console import console
from .expense import Constraint
from .expense import Expense
from .expense import Period
from .expense import Status
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
        table = self._generate_table(
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

    def _generate_table(
        self,
        expenses: List[Expense],
        title: str = "",
        caption: str = "",
        focus: Optional[int] = None,
    ) -> Table:
        """Generate a rich table from a list of expenses."""
        table = Table(title=title, box=box.MINIMAL, caption=caption, caption_justify="right", expand=True)
        table.add_column("#", justify="center")
        table.add_column("Date", justify="left", style="orange1")
        table.add_column("Time", justify="left", style="orange1")
        table.add_column("Amount", justify="right", style="red")
        table.add_column("Merchant", style="cyan", justify="left")
        table.add_column("Category", style="dim white", justify="left")
        table.add_column("Status", style="white", justify="left")
        table.add_column("I Paid", style="white", justify="right")
        table.add_column("Payback", style="white", justify="left")
        table.add_column("Type", style="white", justify="left")
        table.add_column("Period", style="white", justify="left")
        table.add_column("Comment", style="white", justify="left")

        for i, t in enumerate(expenses):
            # Convert timestamp to date
            timestamp = int(t.timestamp) / 1000
            ts_date = (
                datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.UTC).astimezone(pytz.timezone("Europe/Paris"))
            )
            day_name_str = ts_date.strftime("%A")[:3]
            day_nth_str = ts_date.strftime("%d")
            month_str = ts_date.strftime("%B")
            time_str = ts_date.strftime("%H:%M")
            date_str = f"{day_name_str} {day_nth_str} {month_str[:3]}"

            # Format amount with colors
            amount_color = "" if t.amount < 0 else "[green]"
            amount_str = f"{amount_color}{t.amount:.2f} €"

            # Format i_paid with colors just as amount
            i_paid_color = "[green]" if t.i_paid is not None and t.i_paid > 0 else ""
            i_paid_str = f"{i_paid_color}{t.i_paid:.2f} €" if t.i_paid is not None else ""

            # Add a separator between months
            separator = False
            if len(expenses) > 1 and i < len(expenses) - 1:
                np1_month_str = datetime.utcfromtimestamp(int(expenses[i + 1].timestamp) / 1000).strftime("%B")
                separator = bool(month_str != np1_month_str)

            # If focus is set, highlight the corresponding row and dim the others
            if focus is not None:
                style = "bold" if i == focus else "dim"
            else:
                style = "dim" if "(transfer)" in t.merchant_name else "none"

            # Add the row to the table
            table.add_row(
                str(t.cell_number),
                date_str,
                time_str,
                amount_str,
                t.merchant_name,
                t.merchant_category[:30],
                str(t.status.value).capitalize() if t.status != Status.UNKNOWN else "",
                i_paid_str,
                t.payback,
                str(t.constraint.value).capitalize() if t.constraint != Constraint.UNKNOWN else "",
                str(t.period.value).capitalize() if t.period != Period.UNKNOWN else "",
                t.comment,
                style=style,
                end_section=separator,
            )

        return table
