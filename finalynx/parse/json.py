import json

from ..assistant import Assistant
from ..portfolio.bucket import Bucket
from ..portfolio.envelope import Envelope
from ..portfolio.folder import Portfolio
from .parser import Parser


class ImportJSON(Parser):
    """JSON configuration deserializer to an `Assistant` instance."""

    def _parse_data(self) -> Assistant:
        """:returns: An `Assistant` instance with a full configuration definition."""

        # Read the configuration file to a dictionary
        json_dict = json.loads(self.data)

        # Generate object instances from the dictionary
        envelopes = [Envelope.from_dict(e) for e in json_dict["envelopes"]]
        buckets = [Bucket.from_dict(b, {e.name: e for e in envelopes}) for b in json_dict["buckets"]]
        portfolio = Portfolio.from_dict(
            json_dict["portfolio"],
            {b.name: b for b in buckets},
            {e.name: e for e in envelopes},
        )

        # Return a fully populated Assistant instance
        return Assistant(portfolio, buckets, envelopes, enable_export=False)
