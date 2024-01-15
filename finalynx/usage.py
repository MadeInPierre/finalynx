import sys

from .__meta__ import __version__

# When using finalynx from `python -m finalynx ...`, add additional usage requirements
main_usage = "--json=input-file "

main_options = """
  --json=input-file    When calling Finalynx in standalone mode, a JSON configuration file is mandatory
"""


# Add standalone usage only when finalynx is not called through a custom python script
def main_filter(message: str) -> str:
    return message if ".py" not in sys.argv[0] else ""


# Define the finalynx command-line usage which varies depending on how it's called.
# When "sys.argv[0]" is the path to a python script, it means the user is using its own script.
# Otherwise, the user is using
__doc__ = f"""
Finalynx command line v{__version__}
Usage:
  finalynx {main_filter(main_usage)}[ideal | target | delta | perf | text | --format=string] [--no-export | --export-dir=path] [--sidecar=format]... [budget] [dashboard] [options]
  finalynx (-h | --help)
  finalynx (-v | --version)

Options:
  -h --help            Show this help message and exit
  -v --version         Display the current version and exit

  -i --ignore-orphans  Ignore fetched lines that you didn't reference in your portfolio
  -c --clear-cache     Delete any data from Finary that was cached locally
  -f --force-signin    Clear cache, cookies and credentials files to sign in again
  -a --hide-amounts    Display your portfolio with dots instead of the real values (easier to share)
  -d --show-data       Show what has been fetched online (e.g. from your Finary account)
  -r --hide-root       Display your portfolio without the root (cosmetic preference)
{main_filter(main_options)}
  dashboard            Launch an interactive web dashboard!

  budget               Check your daily expenses (N26 accounts only for now)
  -I --interactive     Interactively review and classify your expenses (requires budget option)

  --no-export          Don't export to JSON
  --export-dir=path    Path to a folder where the JSON file will be saved

  -t --theme=string    Choose a predefined color theme for the console output (light or dark)
  --sidecar=string     Output format for each sidecar (can be repeated), defaults to "[delta]"
  --format=string      Customize the maint tree's output format to your own style and information
  ideal                Shortcut to --format="[console_ideal]" (show ideal amounts to follow all targets)
  target               Shortcut to --format="[console_target]" (show target values instead of amounts)
  delta                Shortcut to --format="[console_delta]" (show deltas instead of amounts)
  perf                 Shortcut to --format="[console_perf]" (show expected performances)

  -s --sources=string  Comma-separated list of sources to activate, defaults to "finary" only

  --sim-steps=int      Display the simulated portfolio's worth every X years, defaults to 5
  --future             Print the portfolio after the simulation has finished
  --each-step          Print the portfolio for each step of the simulation
  --metric-frequency   Record the portfolio stats on each day of the simulation 'DAY', 'MONTH', 'YEAR'

"""
