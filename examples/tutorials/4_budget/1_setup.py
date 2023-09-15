"""
Finalynx - Tutorial 4.1 - Track your daily expenses
===================================================


This tutorial shows how to track your daily expenses by using the `Budget`
class.


Try it out by running:
> python3 examples/tutorials/12_envelopes.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio


""" [FIRST SETUP] -------------------------------------------------------
Finalynx's budget feature requires a Google Sheets spreadsheet to store
your expenses and personal classofications. This spreadsheet must be
created manually before running the assistant for the first time and
named "Finalynx Expenses".

The spreadsheet must have the following column names in the first row:
- Timestamp
- Amount
- Merchant
- Category
- STATUS
- I PAID
- PAYBACK
- CONSTRAINT
- PERIOD
- Comment

The document must be shared with the email address of the service account
created in the Google Cloud Platform. Follow this tutorial to create a
personal service account (5 first minutes only):
> https://youtu.be/bu5wXjz2KvU

Then, download the JSON file containing the credentials of the service
account and save it in your OS's default directory:
- Linux: ~/.config/gspread/service_account.json
- Windows: %APPDATA%/gspread/service_account.json
"""


""" [USAGE] -------------------------------------------------------------
The first 4 columns will be filled by the assistant. The other columns
are used to classify your expenses.
- The `STATUS` column is used to classify your expenses as `TODO` if you
still need to do something about it (e.g. someone has not paid you back),
or `DONE` if you have nothing to do about it anymore, or `SKIP` to ignore.
- The `I PAID` column is used to set the amount you paid for YOURSELF for
an expense. For instance, if you paid for a restaurant bill for 4 people,
you can set the `I PAID` column to 25% of the total amount.
- The `PAYBACK` column can be used to note who owes you money.
- The `CONSTRAINT` column can be used to classify the importance of an
expense. Accepted values are `FIXED`, `MODULAR`, `NOCHOICE`, `VARIABLE`,
`OPTIONAL`, `HOBBIES`, or `FUN`.
- The `PERIOD` column can be used to say if an expense is `MONTHLY` or
`YEARLY` (cost divided by 12 and spread to all months).
- The `Comment` column can be used to add any note to an expense.

Once you have run the assistant, it will fill the Google Sheets with your expenses from N26.
Then, you can either manually classify your expenses in the Google Sheets, or you can run
the assistant again with the `interactive` option set to `True` to enter the interactive
mode and classify your expenses from the console.
"""


# Your usual portfolio configuration here
portfolio = Portfolio()

# Use `check_budget=True` to enable the budget feature, and `interactive=True` to
# classify your expenses from the console.
assistant = Assistant(portfolio, check_budget=True, interactive=False)

# Optionally, you can set the path to the Google Sheets token file before running the assistant.
# By default, it will look for gpsread's default locations depending on your OS.
assistant.budget.set_gspread_token_path("your/path/to/service_account.json")

# Assistant will connect to the Google Sheets and N26 APIs to save and display your expenses.
assistant.run()


""" [COMMAND LINE] ------------------------------------------------------------
You can also control the interactive mode from the command line:
"""
# > python your_config.py -I (same as --interactive)
