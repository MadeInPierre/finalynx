# 🎨 Customization

## 🧑‍💻 Command-line options
There are three ways to configure options in Finalynx:

A. **From the `Assistant` class:**
```py
Assistant(option1=value1, ...)
```
B. **From a custom Python script:**
```sh
python your_config.py [options]
```
C. **From Finalynx's standalone mode:**
```sh
python -m finalynx --json=your_config.json [options]
```

See the full list of available options below:
```md
Usage:
  finalynx [--json=input-file] [--format=string] [dashboard] [options]
  finalynx (-h | --help)
  finalynx (-v | --version)

Options:
  -h --help            Show this help message and exit
  -v --version         Display the current version and exit

  # Only valid when calling `python -m finalynx`
  --json=input-file    When calling Finalynx in standalone mode, JSON file is mandatory

  --format=string      Customize the output format to your own style and information

  -i --ignore-orphans  Ignore fetched lines that you didn't reference in your portfolio
  -c --clear-cache     Delete any data from Finary that was cached locally
  -f --force-signin    Clear cache, cookies and credentials files to sign in again
  -a --hide-amounts    Display your portfolio with dots instead of the real values
  -r --hide-root       Display your portfolio without the root (cosmetic preference)
```

## 🌈 Output format
It is possible to specify a custom print format to customize the look of your tree:
```sh
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
```sh
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
