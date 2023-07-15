"""
This module contains the logic for displaying a table of expenses. It is only used
internally by the `Budget` class.
"""
from datetime import datetime
from typing import List
from typing import Optional

from rich import box
from rich.table import Table

from ..config import get_active_theme as TH
from .expense import Constraint
from .expense import Expense
from .expense import Period
from .expense import Status


def _render_expenses_table(
    expenses: List[Expense],
    title: str = "",
    caption: str = "",
    focus: Optional[int] = None,
) -> Table:
    """Generate a rich console table from a list of expenses."""
    table = Table(title=title, box=box.MINIMAL, caption=caption, caption_justify="right", expand=True)
    table.add_column("#", justify="center", style=TH().TEXT)
    table.add_column("Date", justify="left", style="orange1")
    table.add_column("Time", justify="left", style="orange1")
    table.add_column("Amount", justify="right", style="red")
    table.add_column("Merchant", justify="left", style="cyan")
    table.add_column("Category", justify="left", style=TH().HINT)
    table.add_column("Status", justify="left", style=TH().TEXT)
    table.add_column("I Paid", justify="right", style="red")
    table.add_column("Payback", justify="left", style=TH().TEXT)
    table.add_column("Type", justify="left", style=TH().TEXT)
    table.add_column("Period", justify="left", style=TH().TEXT)
    table.add_column("Comment", justify="left", style=TH().HINT)

    for i, t in enumerate(expenses):
        # Format date and time
        ts_date = t.as_datetime()
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
