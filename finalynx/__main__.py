"""
This file describes finalynx's behavior when called as a standalone python package like {code}`python -m finalynx [options]`.

Currently, Finalynx does not support direct calls and only prints the command-line usage description to the console.
"""
from docopt import docopt

from .__meta__ import __version__
from .parse.json import ImportJSON
from .usage import __doc__

if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)

    # If a configuration file was provided, parse it and run the assistant
    if args["--json"]:
        assistant = ImportJSON(args["--json"]).parse()
        assistant.run()

    # If no input was provided while calling finalynx in standalone mode (i.e. this file), exit with usage
    else:
        print(__doc__)
