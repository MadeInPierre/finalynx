"""
Finalynx - Tutorial 8 - Define buckets to group similar lines
=============================================================

This tutorial shows how to define buckets to group similar lines together.
Buckets are useful to group lines by type, by account, by risk level, etc.
For instance, if you have multiple Livrets, you can group them in a bucket
to treat them as a single investment.

Try it out by running:
> python3 examples/tutorials/8_buckets.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio, Folder, Line
from finalynx import Bucket, SharedFolder


""" [BUCKETS] -----------------------------------------------------------------
A `Bucket` object is a special object that holds a list of `Line` objects.
All lines in a bucket are treated as a single investment.
"""
bucket_livrets = Bucket(
    "My Bucket",
    [
        # Set random amounts manually to make a cool result when you run this tutorial
        Line("Livret Jeune", amount=1500),
        Line("Livret A", amount=23000),
        Line("LDDS", amount=6000),
    ],
)


""" [USING BUCKETS] ------------------------------------------------------------
You can only use buckets with `SharedFolder` objects. All `SharedFolder`s that
use the same bucket will progressively use the total amount contained in the
bucket one-by-one, until the bucket is empty.

Every `SharedFolder` will use a `target_amount` attribute to define how much
it should use from the bucket, except for the last `SharedFolder` which will
will NOT use `target_amount` to use what's left in the bucket.
"""


portfolio = Portfolio(
    "My Portfolio",
    children=[
        SharedFolder("Safety savings", bucket=bucket_livrets, target_amount=5000),
        SharedFolder("Medium term", bucket=bucket_livrets, target_amount=10000),
        Folder(
            "Long term",
            children=[
                SharedFolder("Livrets surplus", bucket=bucket_livrets),  # Will use what's left
                Folder(
                    "Stocks",
                    children=[
                        Line("ETF World"),
                    ],
                ),
            ],
        ),
    ],
)


# Run the assistant, it will fetch the data from Finary distribute the amounts
# in the buckets to the SharedFolders that use them.
Assistant(
    portfolio,
    buckets=[bucket_livrets],
    ignore_orphans=True,  # Simply used to make the result nicer when you run this tutorial
).run()
