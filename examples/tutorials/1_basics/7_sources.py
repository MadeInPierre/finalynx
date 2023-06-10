"""
Finalynx - Tutorial 7 - Fetch data from Finary and other sources
================================================================


This tutorial shows how to launch an interactive dashboard to explore your
portfolio in a web browser. The dashboard is currently in experimental mode,
and contributors with web development skills are warmly welcome to improve it!

See the available sources in the source code directly, please contribute! :)
> https://github.com/MadeInPierre/finalynx/blob/main/finalynx/fetch/


Try it out by running:
> python3 examples/tutorials/7_sources.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio
from finalynx.fetch.source_realt import SourceRealT


# Create a portfolio definition (empty for now)
portfolio = Portfolio()

# Create the assistant instance, and specify the source names to fetch data from
assistant = Assistant(portfolio, active_sources=["finary", "realt1", "realt2"])

# Add a source to fetch data from RealT
assistant.add_source(SourceRealT("0xMY_REALT_API_KEY", name="realt1"))  # Default is realt

# Fetch from a second account from the same source
assistant.add_source(SourceRealT("0xMY_REALT_API_KEY_2", name="realt2"))

# Run the assistant
assistant.run()


""" [COMMAND LINE] ------------------------------------------------------------
You can also control the launch from the command line. Sources must be added
from the python configuration file above, but you can control which ones to
activate from the command line:
"""
# > python your_config.py --sources="finary,realt1"
