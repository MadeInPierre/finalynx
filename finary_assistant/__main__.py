"""
Finary Assistant command line
Usage:
    python your_config.py [options]

Options:
  -t --todo      TODO

"""
from docopt import docopt
from .__init__ import __version__

if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)

    if args["todo"]:
        print("TODO")
    