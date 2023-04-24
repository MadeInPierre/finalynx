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
  finalynx {main_filter(main_usage)}[ideal | targets | deltas | perf | text | --format=string] [--no-export | --export-dir=path] [dashboard] [options]
  finalynx (-h | --help)
  finalynx (-v | --version)

Options:
  -h --help            Show this help message and exit
  -v --version         Display the current version and exit
{main_filter(main_options)}
  dashboard            Launch an interactive web dashboard!

  --no-export          Don't export to JSON
  --export-dir=path    Path to a folder where the file will be saved

  --hide-deltas        Don't show delta investment recommendations next to the tree
  --format=string      Customize the output format to your own style and information
  ideal                Shortcut to --format="[console_ideal]" (show ideal amounts to follow all targets)
  targets              Shortcut to --format="[console_targets]" (show target values instead of amounts)
  deltas               Shortcut to --format="[console_deltas]" (show deltas instead of amounts)
  perf                 Shortcut to --format="[console_perf]" (show expected performances)
  text                 Shortcut to --format="[console_text]" (no colors)

  -i --ignore-orphans  Ignore fetched lines that you didn't reference in your portfolio
  -c --clear-cache     Delete any data from Finary that was cached locally
  -f --force-signin    Clear cache, cookies and credentials files to sign in again
  -a --hide-amounts    Display your portfolio with dots instead of the real values (easier to share)
  -d --show-data       Show what has been fetched online (e.g. from your Finary account)
  -r --hide-root       Display your portfolio without the root (cosmetic preference)

"""
