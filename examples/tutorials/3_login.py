"""
Finalynx - Tutorial 3 - Control login and cache
===============================================

This tutorial shows how to clear the cache and login again to Finary
if you have changed your password or if you want to refresh your data.

Try it out by running:
> python3 examples/tutorials/3_login.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio


""" [LOGIN] -------------------------------------------------------------------
Finalynx saves your last login session in a cookies file to avoid logging in
each time you run the assistant. If you want to clear the cookies and login
again, set the `force_signin` option to True. This will also clear the cache.
"""


""" [CACHE] -------------------------------------------------------------------
Finalynx also saves your data in a cache file to avoid fetching it from Finary
when you run the assistant many times in a row. The cache is valid for 12 hours
after which Finalynx will fetch the data again from Finary. To force a refresh
before the 12 hours, set the `clear_cache` option to True. This will not clear
the cookies so you don't need to login again.
"""


# Run the assistant with the `clear_cache` and/or `force_signin` options:
Assistant(Portfolio(), clear_cache=True, force_signin=False).run()


""" [COMMAND LINE] ------------------------------------------------------------
You can also control these from the command line:
"""
# > python your_config.py -c (same as --clear-cache)
# > python your_config.py -f (same as --force-signin)
