import json

from finalynx.portfolio.bucket import Bucket
from finalynx.portfolio.envelope import Envelope

from ..assistant import Assistant
from ..portfolio.portfolio import Portfolio
from .parser import Parser


class ImportJSON(Parser):
    """JSON configuration deserializer to an `Assistant` instance."""

    def _parse_data(self) -> Assistant:
        """:returns: An `Assistant` instance with a full configuration definition."""
        json_dict = json.loads(self.data)

        # portfolio = Portfolio.from_dict(json_dict["portfolio"])
        buckets = [Bucket.from_dict(b) for b in json_dict["buckets"]]
        envelopes = [Envelope.from_dict(e) for e in json_dict["envelopes"]]
        return Assistant(Portfolio(), buckets, envelopes)
