"""
Finalynx - Tutorial 6 - Launch an interactive dashboard
=======================================================

This tutorial shows how to launch an interactive dashboard to explore your
portfolio in a web browser. The dashboard is currently in experimental mode,
and contributors with web development skills are warmly welcome to improve it!

Try it out by running:
> python3 examples/tutorials/6_dashboard.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio


# Create a portfolio definition (empty for now)
portfolio = Portfolio()

# Run the assistant with the `launch_dashboard` option, then visit the URL:
# > http://127.0.0.1:8000
Assistant(portfolio, launch_dashboard=True).run()  # Defaults to False


""" [COMMAND LINE] ------------------------------------------------------------
You can also control the launch from the command line:
"""
# > python your_config.py dashboard


""" [LAUNCH THE DASHBOARD LATER] ----------------------------------------------
If you want more fine grain control over when to launch the dashboard, don't
use the `launch_dashboard` option and instead use `launch_dashboard()`:
"""
# assistant = Assistant(portfolio)
# assistant.launch_dashboard()
