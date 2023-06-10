"""
Finalynx - Tutorial 4 - Export your portfolio to JSON logs
==========================================================


By default, Finalynx saves your portfolio in a JSON file everytime
you run the assistant in a `logs` folder. Each log file is named
with the date of the run. You can disable this feature by setting
the `enable_export` option to False.

This tutorial shows how to export your portfolio to a JSON log file.
The log file can be used to import your portfolio in another Finalynx
instance or to keep a backup of your portfolio. In the future, you will
be able to import your portfolio from the log file using the command:
> python -m finalynx --import=your_portfolio_backup.json [other options]


Try it out by running:
> python3 examples/tutorials/4_export.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio


""" [EXPORT] ------------------------------------------------------------------
By default, Finalynx saves your portfolio in a JSON file in the `logs` folder.
You can disable this feature by setting the `enable_export` option to False.
You can also change the export directory by setting the `export_dir` option.
If you see an error about the export directory, try to create it manually first.
"""


# Create a portfolio definition (empty for now)
portfolio = Portfolio()

# Run the assistant with the `enable_export` and/or `export_dir` options:
Assistant(
    portfolio,
    export_dir="logs",  # Relative to the current directory, defaults to "logs"
    enable_export=True,  # Disable the export feature completely, defaults to True
).run()


""" [COMMAND LINE] ------------------------------------------------------------
You can also control these from the command line:
"""
# > python your_config.py --export-dir=path/to/save/logs/dir/
# > python your_config.py --no-export
