"""
This file describes this module's behavior when called as a standalone python package like {code}`python -m finalynx`.

Currently, Finalynx does not support direct calls and only prints the command-line usage description to the console.
"""
from .__init__ import __version__  # type: ignore
from .assistant import __doc__

if __name__ == "__main__":
    print(f"Finalynx v{__version__}", __doc__)
