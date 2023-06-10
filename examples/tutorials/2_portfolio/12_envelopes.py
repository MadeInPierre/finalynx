"""
Finalynx - Tutorial 12 - Set envelopes for your lines
=====================================================


This tutorial shows how to define envelopes for your lines. An envelope is a
container for your money, it can be a bank account, a stock market account, a
crypto wallet, etc. You can set an envelope for each line of your portfolio.

Envelopes are used to:
- Generate graphs and simulations in the dashboard.
- Generate a list of transactions to perform to reach your targets (recommendations)


See the online documentation for the list of available pre-defined envelopes:
> https://github.com/MadeInPierre/finalynx/blob/main/finalynx/portfolio/envelopes.py

Try it out by running:
> python3 examples/tutorials/12_envelopes.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio, Folder, Line
from finalynx import Envelope, AV, PEA, PEE, PER
from datetime import date


""" [ENVELOPES] ---------------------------------------------------------------
Use the `envelope` argument to set an envelope for a line or folder. It can be
initialized with the following arguments:
- `name`: the name of the envelope, displayed everywhere in Finalynx
- `code`: displayed name in the console tree (3 characters recommended)
- `key`: the name of the envelope in Finary if different from `name`
- `date_created`: the date when the account was created (used for graphs and simulations)
- `date_unlock`: the date when you will be allowed to withdraw money from this envelope
- `date_untax`: the date when you will be allowed to withdraw money without additional taxes
"""


# Minimal example, "My Bank" must also be the account name in Finary
env_bank1 = Envelope("My Bank", "BNK")

# Use the key argument to specify the name in Finary ()"My Bank" becomes the display name)
env_bank2 = Envelope("My Bank", "BNK", key="NAME_IN_FINARY")

# Set a date when the account was created, used for graphs in the dashboard
env_bank3 = Envelope("My Bank", "BNK", date_created=date(2021, 1, 1))

# Full example with all available arguments
env_bank4 = Envelope(
    "My Bank",
    "BNK",
    date_created=date(2021, 1, 1),
    date_unlock=date(2026, 1, 1),
    date_untax=date(2030, 1, 1),
    key="NAME_IN_FINARY",
)


""" [SHORTCUTS] ---------------------------------------------------------------
Finalynx includes a few shortcuts to create common envelopes for common use
cases (they are French for now, feel free to contribute or request for others):
"""
# Specify the creation date, `unlock` date will be the same and `untax` 8 years later
env_av = AV("My AV", "AV ", date(2021, 1, 1))

# Specify the creation date, unlock/tax dates will be 5 years later
env_pea = PEA("My PEA", "PEA", date(2021, 1, 1))

# Same as PEA but you can override dates if you want
env_pee = PEE("My PEE", "PEE", date(2021, 1, 1))

# Retirement date will be the unlock and untax dates
env_per = PER("My PER", "PER", date(2021, 1, 1), date_retirement=date(2050, 1, 1))


""" [AUTO FILL] ---------------------------------------------------------------
When specifying an envelope to a folder, all lines fetched from Finary and other
sources with the same account name will be automatically assigned to this folder.
"""


portfolio = Portfolio(
    "My Portfolio",
    children=[
        # Assign an envelope to a line, will be used in the dashboard and investment recommendations
        Line("Line 1", envelope=env_bank1),
        # This folder will be automatically filled with all lines from the AV envelope
        Folder("Autofilled folder", envelope=env_av),
        # This folder will set its own envelope to all children, and also autofill new lines from Finary
        Folder(
            "Folder 2",
            envelope=env_pea,
            children=[
                # This line will inherit the parent folder's envelope
                Line("Line 2"),
                # This line will override the parent folder's default envelope
                Line("Line 3", envelope=env_bank2),
                # Subfolders and sublines will also inherit the parent folder's envelope
                Folder("My subfolder", children=[Line("Line 4")]),
                # Finally, new lines from Finary with the same account name will be
                # automatically assigned to this folder, unless they have already
                # been declared somewhere above in the portfolio tree.
            ],
        ),
    ],
)


# Run the assistant (nothing cool will happen if you run this tutorial, it's just for the completeness)
Assistant(portfolio).run()
