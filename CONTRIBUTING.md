# Contributors
First, thank you for contributing! 💝

Any contribution of any skill level is highly appreciated and welcome. Feel free to chat about what you would like to do in the [finary forum](TODO) or in this repo's [discussions](https://github.com/MadeInPierre/finary_assistant/discussions/new/choose) space.

### 🤔 Philosophy
The current goal of this project is to create a minimalistic but visual and informative tool to see our portfolios in new ways. While Finary provides nice graphs already, this project aims to freely explore other ideas.

Currently, this project is a command-line tool but it may be extended to other output formats (Web dashboard, PDF report, Jupyter notebook, ...) depending on the features we'll want to add. Please feel free to open a [new discussion](https://github.com/MadeInPierre/finary_assistant/discussions/new/choose) to share your ideas and help shape this project! If you have any skill you would like to leverage here (e.g. web development), then let's use that 🍀

### 🔧 Architecture
The project structure is pretty typical for Python projects, with `finary_assistant` being the source directory. The main entry point is `assistant.py` with the `Assistant` class, which orchestrates the fetching, processing, and printing steps. Each feature domain is separated in its own submodule:
  - `portfolio/` is responsible for building and displaying the portfolio tree, with basic processing tools such as investment targets.
  - `fetch/` is reponsible of using `finary_api` to fetch the amounts into the `portfolio` tree.
  - `finary_api/` is a git submodule since finary_api is not available on PyPI (the repository for `pip`). Hence, we include its source code inside our own `pip` package.
  - `simulator/` and `copilot/` are empty for now and will be developed later. Please checkout the [project management](https://github.com/users/MadeInPierre/projects/4) and GitHub issues to see what's planned next.

Feel free to suggest additions or changes!

### 🌊 Contribution workflow
If you want to propose something new (new feature, extension, bugfix, documentation help, ...), please follow these steps:
1. **Fork** this repo (click the _fork_ button on GitHub)
2. **Follow the initial setup** described in the section below
3. **Create a separate branch** that will hold your contribution
4. **Make your changes** 🪄
5. **Stage your changes** to git using `git add .`
6. **Check your changes** with `pre-commit run`. If some of your changes do not follow the conventions, they will automatically be fixed. Check the proposed changes and run `git add . && pre-commit run` again until all checks pass.
7. **Commit** your contributions using the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) naming standard
8. **Push** your changes to your remote fork
9. **Open a pull-request** to our primary repo and target the `main` branch
10. **Wait for review**: let's chat about it in the pull request comments and merge it 🎉

For your next contributions, you can simply update your fork and start from step 3. Let me know if you plan on actively contributing to this project, I can give you direct access to this repo.

### ⚙️ Initial setup
1. Clone this repository using the `--recursive` option to include the [`finary_api`](https://github.com/lasconic/finary) submodule:
```sh
git clone --recursive https://github.com/MadeInPierre/finary_assistant.git
cd finary_assistant/
# If you forgot --recursive: git submodule update --init --recursive
```
2. Install [`poetry`](https://python-poetry.org/) which manages the project dependencies, and get all dependencies needed to work on this project:
```sh
pip3 install poetry && poetry check && poetry install
```
3. Try the assistant with:
```sh
python examples/demo.py
```
If you see a template portfolio tree and your investments detected from Finary, then you're now part of the (small) team! 🎉 Now create your own copy of the demo file and go customize it for your own needs (the name `assistant_config` is recommended as it is ignored from git):
```sh
cp examples/demo.py assistant_config.py  # <- Your own portfolio here
```
4. When you're ready to make a contribution: this project uses [`pre-commit`](https://pre-commit.com) to make sure we all use the same code styling and formatting conventions. Make sure to activate it on this repo using:
```sh
pre-commit install
```
5. Now, each time you commit, a list of checks will run on the files you changed. You can try it out before committing with:
```sh
pre-commit run  # -a if you want to check all files in the repo
```

When you commit, make sure to follow the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) standard for your commit messages, which will be used to automatically change the release version.

- ⚠️ **Note:** VSCode seems to bypass these checks if you commit from the GUI. Don't forget to run pre-commit in a terminal to make sure your commit is tidy, and then commit in the GUI.

You can now push your changes to your fork (preferably in a separate branch if you plan on contributing again) and create a pull request on the original repo.

### ♻️ Continuous Integration
The original repo has an automated CI/CD pipeline setup for two tasks:
1. Run the pre-commit checks on any new pull request or push to report if something was forgotten.
2. When something is pushed to the `main` branch (e.g. a merge from your pull request), a job calculates the new version for `finary_assistant` based on the commit messages, updates the [changelog](https://github.com/MadeInPierre/finary_assistant/blob/main/CHANGELOG.md), creates a [release](https://github.com/MadeInPierre/finary_assistant/releases) on GitHub, and publishes the new package to [PyPI](https://pypi.org/project/finary-assistant/).

### ❓ Missing stuff for now
There are no tests and published documentation for now. Ping me if you want me/us to set them up.
