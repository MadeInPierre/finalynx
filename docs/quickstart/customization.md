# 🎨 Customization

## 🧑‍💻 Command-line options
There are three ways to configure options in Finalynx:

A. **From the `Assistant` class:**
```python
portfolio = Portfolio(...)  # <- your config
Assistant(portfolio, option1=value1, ...).run()
```
B. **From a custom Python script:**
```bash
python your_config.py [options]
```
C. **From Finalynx's standalone mode:**
```bash
python -m finalynx --json=your_config.json [options]
```

See the full list of available options by running:
```bash
python your_config.py --help
```

## 🌈 Output format
It is possible to specify a custom print format to customize the look of your tree:
```bash
python your_config.py --format="your format"                 # shell
python -m finalynx --json=input.json --format="your format"  # shell
Assistant(output_format="your format", other_arguments...)   # python
```

`Line` and `Folder` objects have a `render()` method which accepts a custom format. Here are the aliases currently defined for them:

```py
# Print all elements with colors to obtain a beautiful tree
"[console]": "[target][dim white][prehint][/] [name_color][name][/] [dim white][hint]",

# Same without color, useful for exporting in places without color support
"[text]": "[target_text][prehint] [name] [hint]",

# Alias to render the full target element (color, symbol, amount, curency)
"[target]": "[[target_color]][target_text][/]",

# Same as previous but without color
"[target_text]": "[target_symbol] [amount] [currency]",
```

Here are some examples of valid formats:
```bash
python your_config.py --format="[console]"  # Default, prints the full colored tree
python your_config.py --format="[text]"  # Print the full tree but colorless
python your_config.py --format="[blue][amount] [name][/]"  # Use [/] to reset the color
python your_config.py --format="[target_color][name][/]"  # You guessed it!
```

```{tip}
<details>
<summary><b>Implementation details</b></summary>

See the API Reference about [`Render`](https://finalynx.readthedocs.io/en/latest/apidocs/finalynx/finalynx.portfolio.render.html) and [`Node`](https://finalynx.readthedocs.io/en/latest/apidocs/finalynx/finalynx.portfolio.node.html) for implementation details. Here is an executive summary:

```python
class Node(Render):
    # Aliases that are simply replaced by a new string for shorter options
    render_aliases: Dict[str, str] = {
        "[alias_name]": "text to be replaced with"
    }

    # Each keywoard has its dedicated method which returns the formatted element
    render_agents: Dict[str, Callable[..., str]] = {
        "keyword": self._render_keyword, # No need for the `[]` brackets
        ...
    }

    # Defined in the abstract `Render` class
    def render(self):
        ... # replaces all aliases recursively, then calls each renderer

    # Example of an 'agent' method
    def _render_target(self):
        return self.target.render(format)
```
</details>

## ⛓ Sidecars

What if you could show additional information along with your main tree with columns on the right that show customizable information, like ideal investment amounts, expected yearly performance, delta investments, and so on?

![screenshot](https://raw.githubusercontent.com/MadeInPierre/finalynx/main/docs/_static/screenshot_full.png)

Meet _sidecars_: each sidecar is a column on the right of the main tree that displays any information about the node on the same console line. It uses the same output format structure defined above.

A sidecar is defined by 4 parameters:
- **Output format:** Specify what you want to render in this column (aka. sidecar). This uses the same format as the "output format" explained above, except it will be rendered in a separate column on the right of the tree.
- **Condition format:** Specify any output format. Only show the output format for each node it this render returns a non-empty string. This is useful to make multiple sidecars work together (e.g. only show ideal amounts if the node requires a non-zero delta transaction).
- **Title:** customize the column (aka. sidecar) title. By default, a title is generated from the output format.
- **Show folders:** A boolean to choose if you want to only show elements for `Line` objects and not `Folder` objects. When set to `False`, only expanded folders will not have any information displayed.

Define your own sidecars using one of two options:
1. From your Python configuration:
```python
assistant = Assistant(
    portfolio,
    sidecars=[
        Sidecar("[ideal]", "[delta]", "HELLO", False),
        Sidecar("[delta]", show_folders=False),
    ],
).run()
```
2. From the command line (comma-separated values):
```bash
python your_config.py --sidecar="[ideal],[delta],HELLO,False" --sidecar="[delta],,,False"
```
