"""
This module contains the logic for reviewing the expenses. It is only used
internally by the `Budget` class.

The `_review()` method of the `Budget` class will display the list of pending
expenses in a nice rich table and ask the user to review them one by one.
"""
from typing import Callable
from typing import List
from typing import Optional

from rich.table import Table

from ..console import console
from ._render import _render_expenses_table
from .expense import Constraint
from .expense import Expense
from .expense import Period
from .expense import Status


N_CONTEXT_ITEMS = 3  # TODO place in config


def _render_mini_expenses_table(expenses: List[Expense], i_focus: int) -> Table:
    """Render a mini table with the current expense in focus and a few
    surrounding expenses. This is used to display the current expense in
    context when asking the user to review it."""
    n_expenses = len(expenses)
    i_min, i_max = max(0, i_focus - N_CONTEXT_ITEMS), min(n_expenses - 1, i_focus + N_CONTEXT_ITEMS)
    i_focus = i_focus - i_min
    return _render_expenses_table(
        expenses[i_min : i_max + 1],  # noqa: E203
        title=f"Reviewing expense {i_focus+1} of {n_expenses}",
        focus=i_focus,
    )


def _ask(
    expenses: List[Expense],
    i_expense: int,
    message: str,
    is_valid: Callable[[str], bool],
    current: Optional[str] = None,
    default: Optional[str] = None,
) -> str:
    """Ask the user to input a value. The input will be validated with the `is_valid` function.
    - If the input is not valid, the user will be asked to try again.
    - If the input is valid, it will be returned.
    - If the input is empty, the `default` value will be returned.
    """
    valid: Optional[bool] = None
    user_input: str = ""

    while valid is not True:
        console.clear()
        console.print(_render_mini_expenses_table(expenses, i_expense))
        console.print(message)

        if current not in [None, ""]:
            console.print(f"[yellow]Current value is: {current}[/]")

        if valid is False:
            console.print("[red]Invalid input, please try again:[/]")

        user_input = console.input("> ").strip()
        if default is not None and user_input == "":
            user_input = default

        valid = is_valid(user_input)

    return user_input


def _set_field(
    expenses: List[Expense],
    i_expense: int,
    question: str,
    options: str,
    is_valid: Callable[[str], bool],
    apply: Callable[[str], bool],
    current: Optional[str] = None,
    default: Optional[str] = None,
) -> Optional[bool]:
    """Ask the user to set a field of the expense. The input will be validated with the `is_valid`
    function. If the input is not valid, the user will be asked to try again. If the input is valid,
    the `apply` function will be called with the input as argument. If the input is empty, the
    `default` value will be used instead.
    """
    message = (
        f"\n\n{question}\n"
        f"{options}\n"
        "  - [bold green]S[/][dim] to skip this expense[/]\n"
        "  - [bold green]s[/][dim] to skip this field[/]\n"
        "  - [bold green]q[/][dim] to quit[/]\n"
    )

    def is_valid_default(s: str) -> bool:
        return s in ["S", "s", "q"] or is_valid(s)

    result = _ask(expenses, i_expense, message, is_valid_default, current, default)

    if result == "S":
        return False
    elif result == "s":
        return True
    elif result == "q":
        console.clear()
        return None
    return apply(result)


def _i_paid(expenses: List[Expense], i_expense: int) -> Optional[bool]:
    """Ask the user to set the amount they paid for the expense."""
    question = "How much did you pay for yourself?"
    options = (
        "  - [bold green]f[/][dim]     to pay the full amount [bold](default)[/][/]\n"
        "  - [bold green]h[/][dim]     to pay half of the amount[/]\n"
        "  - [bold green]0[/][dim]     to ignore this expense[/]\n"
        "  - [bold green]-1.99[/][dim] to specify an amount[/]\n"
        "  - [bold green]19%[/][dim]   to specify a ratio[/]\n"
    )

    def is_valid(s: str) -> bool:
        if s in ["f", "h", "0"]:
            return True
        elif "%" in s:
            return s.replace("%", "", 1).replace(".", "", 1).strip().isdigit()
        return s.replace("€", "", 1).replace("-", "", 1).replace(".", "", 1).strip().isdigit()

    def apply(s: str) -> bool:
        if s == "f":
            expenses[i_expense].i_paid = expenses[i_expense].amount
        elif s == "h":
            expenses[i_expense].i_paid = expenses[i_expense].amount / 2
        elif s == "0":
            expenses[i_expense].i_paid = 0
        elif "%" in s:
            percentage = float(s.replace("%", "", 1)) / 100
            expenses[i_expense].i_paid = expenses[i_expense].amount * percentage
        else:
            mul = -1 if bool(s[0] == "-") != bool(expenses[i_expense].amount < 0) else 1
            expenses[i_expense].i_paid = float(s) * mul
        return True

    current = str(expenses[i_expense].i_paid) if expenses[i_expense].i_paid is not None else None
    return _set_field(expenses, i_expense, question, options, is_valid, apply, current, default="f")


def _payback(expenses: List[Expense], i_expense: int) -> Optional[bool]:
    """Ask the user to set the payback for the expense (who also paid for this)."""
    question = "Anyone needs to pay you back?"
    options = (
        "  - [bold green]no[/][dim]     this expense only concerns yourself [bold](default)[/][/]\n"
        "  - [bold green]<text>[/][dim] to remind yourself about who participated[/]\n"
    )

    def apply(s: str) -> bool:
        expenses[i_expense].payback = s
        return True

    current = expenses[i_expense].payback
    return _set_field(expenses, i_expense, question, options, lambda _: True, apply, current, default="no")


def _constraint(expenses: List[Expense], i_expense: int) -> Optional[bool]:
    """Ask the user to set the constraint for the expense."""
    question = "How important was this expense?"
    options = "\n".join(
        [
            f"  - [bold green]{c.value[0].lower()}[/][dim] for {c.value.capitalize()}[/]"
            for c in Constraint
            if c != Constraint.UNKNOWN
        ]
    )

    def is_valid(s: str) -> bool:
        return s in [c.value[0].lower() for c in Constraint if c != Constraint.UNKNOWN]

    def apply(s: str) -> bool:
        d_options = {c.value[0].lower(): c.value for c in Constraint if c != Constraint.UNKNOWN}
        expenses[i_expense].constraint = Constraint(d_options[s])
        return True

    current = (
        expenses[i_expense].constraint.value.capitalize()
        if expenses[i_expense].constraint != Constraint.UNKNOWN
        else None
    )
    return _set_field(expenses, i_expense, question, options, is_valid, apply, current)


def _period(expenses: List[Expense], i_expense: int) -> Optional[bool]:
    question = "How should this expense count in your budget?"
    options = (
        "  - [bold green]m[/][dim] for a monthly expense [bold](default)[/][/]\n"
        "  - [bold green]y[/][dim] for a yearly expense[/]\n"
    )

    def is_valid(s: str) -> bool:
        return s in ["m", "y"]

    def apply(s: str) -> bool:
        d_options = {"m": Period.MONTHLY, "y": Period.YEARLY}
        expenses[i_expense].period = Period(d_options[s])
        return True

    current = expenses[i_expense].period.value.capitalize() if expenses[i_expense].period != Period.UNKNOWN else None
    return _set_field(expenses, i_expense, question, options, is_valid, apply, current, default="m")


def _comment(expenses: List[Expense], i_expense: int) -> Optional[bool]:
    question = "Any comments?"
    options = "  - [bold green]<text>[/][dim] for any personal notes[/]\n"

    def apply(s: str) -> bool:
        expenses[i_expense].comment = s
        return True

    current = expenses[i_expense].comment
    return _set_field(expenses, i_expense, question, options, lambda _: True, apply, current)


def _status(expenses: List[Expense], i_expense: int) -> Optional[bool]:
    question = "What's the status of this expense?"
    options = (
        "  - [bold green]t[/] or [bold green]todo[/][dim] to review this expense again next time [bold](default)[/][/]\n"
        "  - [bold green]d[/] or [bold green]done[/][dim] to mark this expense as reviewed[/]\n"
    )

    def is_valid(s: str) -> bool:
        return s.lower() in ["t", "todo", "d", "done"]

    def apply(s: str) -> bool:
        expenses[i_expense].status = Status.DONE if s.lower() in ["d", "done"] else Status.TODO
        return True

    current = expenses[i_expense].status.value.capitalize() if expenses[i_expense].status != Status.UNKNOWN else None
    return _set_field(expenses, i_expense, question, options, is_valid, apply, current, default="t")
