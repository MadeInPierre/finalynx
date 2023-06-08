"""
Finalynx - Tutorial 7 - Define your portfolio structure (basics)
================================================================

This tutorial shows how to define your portfolio structure in your configuration
file. This is the most important part of your configuration and lets you freely
organize your investments in a tree structure.

Try it out by running:
> python3 examples/tutorials/7_structure.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio
from finalynx import Folder, Line


""" [THE BASICS] ---------------------------------------------------------------
The portfolio structure is defined by creating a tree of `Node` objects (abstract
class). Nodes can be `Line`, `Folder` or `SharedFolder` objects. The root of the
tree must be a `Portfolio` object.

A `Line` object represents a single investment. It can have a name, a symbol and
an amount. The symbol is optional and can be used to fetch data from Finary. The
amount is also optional and can be used to override the amount fetched from Finary.

A `Folder` object can have a name and a list of children. The children can be
Line objects or other Folder objects. This lets you organize your investments
in a completely free structure. Folders can be used to group investments by
type, by account, by risk level, etc depending on your needs.

A `SharedFolder` object is similar to a Folder object but holds a `Bucket` object
instead of a list of children. We'll see how to use them in the next tutorial.
"""


portfolio = Portfolio(
    "My Portfolio",  # Only used for display purposes
    currency="€",  # Set the default currency for all children
    target=None,  # We'll see how to use targets later
    children=[
        Folder(
            "My first folder",
            children=[
                # Valid if the name is the same in Finary:
                Line("My 1st investment"),
                # Set the key if you want to set a different display name:
                Line("My 2nd investment", key="ID_IN_FINARY"),
                # Set the currency if you want to override the default:
                Line("My 3rd investment", key="ID_IN_FINARY", currency="$"),
                # Set the amount if you want to override the amount fetched:
                Line("My 4th investment", key="ID_IN_FINARY", amount=1000),
                # Skip a line in the console for aesthetics:
                Line("My 5th investment", key="ID_IN_FINARY", newline=True),
            ],
        ),
        Line("Look ma, new line!"),
    ],
)


# Run the assistant with your custom portfolio structure
Assistant(portfolio).run()
