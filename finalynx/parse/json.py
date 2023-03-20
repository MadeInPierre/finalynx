import json

from ..assistant import Assistant
from ..console import console
from ..portfolio.portfolio import Portfolio
from .parser import Parser


class ImportJSON(Parser):
    """JSON configuration deserializer to an `Assistant` instance."""

    def _parse_data(self) -> Assistant:
        """:returns: An `Assistant` instance with a full configuration definition."""

        json_dict = json.loads(self.data)

        # TODO Create Python objects from the JSON data
        console.log(f"[yellow bold]Warning: JSON parsing not implemented yet, {json_dict=}")
        portfolio = Portfolio(name="Portfolio Name", children=[])

        # TODO Add simulation parameters, copilot, etc once developed
        return Assistant(portfolio)
