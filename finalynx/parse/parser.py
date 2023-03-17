from ..assistant import Assistant
from ..console import console


class Parser:
    """Abstract class that defines a unified interface to all parser subclasses."""

    def __init__(self, filename: str):
        """Abstract class that defines a unified interface to all parser subclasses to remain file type independent.
        :param filename: Relative path to your input file."""
        try:
            self.data = open(filename).read()
        except FileNotFoundError:
            console.log(f"[red bold]Error: File '{filename}' not found, aborting.[/]")
            exit(1)

    def parse(self) -> Assistant:
        """Convert the input file to a fully configured `Assistant` instance."""
        with console.status("[bold green]Parsing input file..."):
            return self._parse_data()

    def _parse_data(self) -> Assistant:
        """Method to be overridden by each parser to return an `Assistant` instance."""
        raise NotImplementedError("Method must be overriden by subclass.")
