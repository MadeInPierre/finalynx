# ✨ Getting Started

The goal is to declare a tree structure of your entire portfolio independently from their host envelopes (e.g. PEA, AV, CTO, etc). Once your entire portfolio strategy is defined here, find the best envelope for each line and add them to your Finary account (manual or automatic sync). Finalynx will fetch each line and display your full portfolio with real-time amounts.

## 🌳 Define your portfolio

To create your portfolio, start with a `Portfolio` object which holds a nested list of `Line`, `Folder`, and `SharedFolder` objects:
- `Line` represents each individual investment. Set the `key` parameter as the name shown in your Finary account if different from the display name.
- `Folder` holds a group of lines or subfolders to create a structure.
- `SharedFolder` accepts a `Bucket` object which groups multiple lines as a single object. You can reference the same bucket multiple times in the tree and set different `bucket_amount` for each shared folder. Each folder will only take the specified amount and let the others below use the rest.

Here is an example of a portfolio structure:
```python
# Create a list of Lines that will be considered as a single Line.
my_bucket = Bucket([
  Line('name_in_finary'),
  Line('My Asset 2', key='name_in_finary'),  # change the display name
  # ...
])

# Define your entire portfolio structure
portfolio = Portfolio('My Portfolio', children=[
  # Add a list of `Line`, `Folder`, and `SharedFolder` objects
  Folder('Short term', children=[
    Line('My Asset 3', key='name_in_finary'),
    SharedFolder('My Folder', bucket=my_bucket, bucket_amount=1000),
    # ...
  ]),
  Folder('Long term', children=[
    # `(Shared)Folders` can be displayed as Expanded (default), Collapsed, or as a Line
    Folder('Stocks', display=FolderDisplay.COLLAPSED, children=[
      SharedFolder('My Folder', bucket=my_bucket),  # display what's left in the bucket
      # ...
    ]),
    # ...
  ])
])
```

```{note}
If you have multiple lines with the same name defined in Finary, you can use Finary's unique ids instead of the name.
Run finalynx with the `--show-data` option which will display all investments along with a unique `id` field.
Then, copy the `id` for each line.

You can use either the `name` or `id` of each line in your portfolio definition:

```python
# Run finalynx and show what has been fetched
python your_config.py --show-data

# Define each line with the investment name or id
Line('CCP N26'),                                              # All three
Line('Neobank', key='CCP N26'),                               # options are
Line('Neobank', key='4ef88718-7de2-45d2-ba63-60d58e912f3e'),  # equivalent
```

## 🎯 Set Targets for each level
Any node in the tree accepts an optional `target` parameter. See the full list of available targets [here](https://github.com/MadeInPierre/finalynx/blob/main/finalynx/portfolio/targets.py):

```python
Folder('Stocks', target=TargetMin(2000, tolerance=500), children=[
  Line('ETF World', key='Amundi ETF ...', target=TargetRatio(80, tolerance=5)),
  # ... Add other lines with the remaining 20% of the Stocks folder.
])
```

## 🚀 Run the assistant
Here is the bare minimum code accepted:
```python
from finalynx import Portfolio, Assistant
portfolio = Portfolio()  # your config here
Assistant(portfolio).run()
```

The `Assistant` class accepts a few options:
```python
Assistant(
    portfolio,
    ignore_orphans=False,  # Ignore fetched lines that you didn't reference in your portfolio.
    force_signin=False,    # Delete your saved credentials and/or cookies session.
    hide_amount=False,     # Hide your portfolio amounts with dots (easier to share).
    hide_root=False,       # Display your portfolio without the root (cosmetic preference).
).run()
```

These options can also be set from the command line, see:
```sh
python your_config.py --help
```

```{tip}
There are other small options here and there, let me know if you're interested (I should write a full documentation). However, you should be good to go with some inspiration taken from [`demo.py`](https://github.com/MadeInPierre/finalynx/blob/main/examples/demo.py).
```
