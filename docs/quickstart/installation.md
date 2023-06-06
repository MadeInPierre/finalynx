# 🔧 Installation

## Quick start

If you don't plan on touching the code, simply run (with python >=3.10 and pip installed):
```sh
pip install finalynx  # run again with --upgrade to update
```

And you're done! Now create your own copy of the [`demo.py`](https://github.com/MadeInPierre/finalynx/blob/main/examples/demo.py) example anywhere and run it to make sure everything works. You can now customize it for your own needs 🚀

```{tip}
**Pro Tip 💡:** Why not setup a script to autorun your config in a new terminal on startup? Could be a nice view 🤭
```

```{note}
**Want to help this project grow?** Checkout the [**contribution guidelines**](https://finalynx.readthedocs.io/en/latest/project/contributing.html) to learn how to install this project in
development mode 🧑‍💻
```

## Detailed instructions

If you need a bit more details, here is a summary of all commands to need to run to make Finalynx work with a basic configuration. First, make sure you have a recent Python version (must be 3.10 or above) by running:

```bash
python3 --version  # Must be >=3.10
```

```{note}
**Note:** If you have any questions or difficulty, please [**open an issue**](https://github.com/MadeInPierre/finalynx/issues/new), we'll be happy to help, teach and learn together! No matter the level, there are no dumb questions right? 🤝
```

There are two options to install Finalynx:

1. Install using `pip`, and paste the contents of the `demo.py` example file in any folder (e.g. Documents):
```bash
pip3 install finalynx        # Automatically install finalynx globally, lets you use `from finalynx import *`
cd somewhere/like/Documents  # Make sure you use any folder outside system files, like your home directory
touch assistant_config.py    # Create your configuration file and past the contents of the `demo.py` example
python3 assistant_config.py  # Run your configuration file to make sure everything works, then customize it!
```

1. Install using `git clone`, lets you modify the code yourself, contribute to this project, and get the latest code to avoid waiting for new releases:
```bash
cd somewhere/like/Documents/  # Choose any folder to download Finalynx's code, must be outside of system folders
git clone https://github.com/MadeInPierre/finalynx.git  # Download the code as a git repository (easy to update)
cd finalynx  # Go inside the newly downloaded project
pip3 install poetry && poetry check && poetry install  # Install all project dependencies
pip3 install -e .  # Install the code globally, -e means you can change the code without the need to reinstall
python3 examples/demo.py  # Try out the demo example to make sure everything works

cp examples/demo.py assistant_config.py  # Create your own copy of the demo, this will be your personal config
# Customize your config now to create your own portfolio!
python3 assistant_config.py --help  # Run your own config (use --help to see customizable options)
```
