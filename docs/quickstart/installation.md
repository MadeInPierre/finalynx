# 🔧 Installation

## Quick start

If you don't plan on touching the code, simply run (with python >=3.10 and pip installed):
```sh
pip install finalynx  # run again with --upgrade to update
```

And you're done! Now create your own copy of the [`demo.py` example file](https://github.com/MadeInPierre/finalynx/blob/main/examples/demo.py) anywhere and run it to make sure everything works. You can now customize it for your own needs 🚀

```{tip}
**Pro Tip 💡:** Why not setup a script to autorun your config in a new terminal on startup? Could be a nice view 🤭
```

## Detailed instructions

If you need a bit more details, here is a summary of all commands to need to run to make Finalynx work with a basic configuration. First, make sure you have a recent Python version (must be 3.10 or above) by running:

```bash
python3 --version  # Must be >=3.10
```

```{note}
**Note:** If you have any questions or difficulty, please [**open an issue**](https://github.com/MadeInPierre/finalynx/issues/new), we'll be happy to help, teach, and learn together! No matter the level, there are no dumb questions right? 🤝
```

There are two options to install Finalynx:

1. **Install using `pip` (beginner-friendly):** open a new terminal and paste the contents of the [`demo.py` example file](https://github.com/MadeInPierre/finalynx/blob/main/examples/demo.py) in any folder, like `Documents` for example:
```bash
# Automatically install finalynx globally, lets you use `from finalynx import *`
pip3 install finalynx

# Make sure you use any folder outside system files, like your home directory
cd somewhere/like/Documents

# Create your configuration file and paste the contents of the `demo.py` example
touch assistant_config.py

# Run your configuration file to make sure everything works, then customize it!
python3 assistant_config.py
```
2. **Install using `git clone`:** lets you modify the code yourself, contribute to this project, and get the latest code to avoid waiting for new releases:
```bash
# Choose any folder to download Finalynx's code, must be outside of system folders
cd somewhere/like/Documents/

# Download the code as a git repository (easy to update)
git clone https://github.com/MadeInPierre/finalynx.git

# Go inside the newly downloaded project
cd finalynx

# Install all project dependencies
pip3 install poetry && poetry check && poetry install

# Install the project globally, -e means you can change the code without reinstalling
pip3 install -e .

# Try out the demo example to make sure everything works
python3 examples/demo.py

# Create your own copy of the demo, this will be your personal config
cp examples/demo.py assistant_config.py

# Customize your config now to create your own portfolio!
python3 assistant_config.py # use --help to see customizable options
```

```{note}
**Want to help this project grow?** Checkout the [**contribution guidelines**](https://finalynx.readthedocs.io/en/latest/project/contributing.html) to learn how to install this project in development mode and agree on common conventions 🧑‍💻
```
