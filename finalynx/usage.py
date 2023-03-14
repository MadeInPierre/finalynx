import sys

from .__meta__ import __version__

# When using finalynx from `python -m finalynx ...`, add additional usage requirements
main_usage = "--json=input-file"

# Define the finalynx command-line usage which varies depending on how it's called.
# When "sys.argv[0]" is the path to a python script, it means the user is using its own script.
# Otherwise, the user is using
__doc__ = f"""
Finalynx command line v{__version__}
Usage:
  finalynx {f"{main_usage} " if ".py" not in sys.argv[0] else ""}[options]

Options:
  -h --help            Show this help message and exit
  -v --version         Display the current version and exit

  -i --ignore-orphans  Ignore fetched lines that you didn't reference in your portfolio
  -f --force-signin    Sign in to Finary even if there is an existing cookies file
  -a --hide-amounts    Display your portfolio with dots instead of the real values (easier to share)
  -r --hide-root       Display your portfolio without the root (cosmetic preference)

"""
