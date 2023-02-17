from docopt import docopt
from .__init__ import __version__
from .assistant import __doc__

if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)
