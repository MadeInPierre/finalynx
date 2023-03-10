# Contribution Guidelines
First, thank you for contributing! 💝

Any contribution of any skill level is highly appreciated and welcome. Feel free to chat about what you would like to do in the [finary forum](https://community.finary.com/t/finary-assistant-aka-finalynx-projet-communautaire-open-source/6498) or in this repo's [discussions](https://github.com/MadeInPierre/finalynx/discussions/new/choose) space.

## 🤔 Philosophy
The current goal of this project is to create a minimalistic but visual and informative tool to see our portfolios in new ways. While Finary provides nice graphs already, this project aims to freely explore other ideas.

Currently, this project is a command-line tool but it may be extended to other output formats (Web dashboard, PDF report, Jupyter notebook, ...) depending on the features we'll want to add. It may also remain as a pure command-line tool using plotting libraries such as [`uniplot`](https://github.com/olavolav/uniplot). Please feel free to open a [new discussion](https://github.com/MadeInPierre/finalynx/discussions/new/choose) to share your ideas and help shape this project! If you have any skill you would like to leverage here (e.g. web development), then let's use that 🍀

## 🔧 Architecture
The project structure is pretty typical for Python projects, with `finalynx` being the source directory. The main entry point is `assistant.py` with the `Assistant` class, which orchestrates the fetching, processing, and printing steps. Each feature domain is separated in its own submodule:
  - `portfolio/` is responsible for building and displaying the portfolio tree, with basic processing tools such as investment targets.
  - `fetch/` is reponsible of using `finary_api` to fetch the amounts into the `portfolio` tree.
  - `finary_api/` is a git submodule since finary_api is not available on PyPI (the repository for `pip`). Hence, we include its source code inside our own `pip` package.
  - `simulator/` and `copilot/` are empty for now and will be developed later. Please checkout the [project management](https://github.com/users/MadeInPierre/projects/4) and GitHub issues to see what's planned next.

Feel free to suggest additions or changes!

## 💬 Project management & Discussions

The most important panel is the 👉 [**Project View**](https://github.com/users/MadeInPierre/projects/4) 👈 to see the current development status. Here is how you can participate:
1. Checkout [**The Plan™**](https://github.com/MadeInPierre/finalynx/discussions/27) to see what's planned for Finalynx in general.
2. Checkout the [**Project View**](https://github.com/users/MadeInPierre/projects/4) to see the current status (which follows the plan's [milestones](https://github.com/MadeInPierre/finalynx/milestones).
3. Open an issue for each of your ideas, even those you don't think you'd develop yourself. Once discussed and assigned to someone in the project view, the development can start.
   - Remember: one issue = one pull request = one feature/bugfix.
4. When you finish a contribution, create a pull request and mention which issue your PR would close. See more details in the next section.

## 🌊 Contribution workflow
If you want to propose something new (new feature, extension, bugfix, documentation help, ...), please follow these steps:
1. **Open an issue** and chat with everyone to make sure your contribution would fit nicely with the project.
1. **Fork** this repo (click the _fork_ button on GitHub)
2. **Follow the initial setup** described in the section below
3. **Create a separate branch** that will hold your contribution
4. **Make your changes** 🪄
5. **Stage your changes** to git using `git add .`
6. **Check your changes** with `pre-commit run`. If some of your changes do not follow the conventions, they will automatically be fixed. Take a look at the proposed changes and run `git add . && pre-commit run` again until all checks pass.
7. **Commit** your contributions using the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) naming standard (e.g. `feat(readme): added something cool`)
8. **Push** your changes to your remote fork
9. **Open a pull-request** to our primary repo and target the `main` branch (using [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) again for your PR title)
10. **Wait for review**: let's chat about it in the pull request comments and merge it 🎉

For your next contributions, you can simply update your fork and start from step 3. Let me know if you plan on actively contributing to this project, I can give you direct access to this repo.

### ⚙️ Initial setup
1. Clone your fork using the `--recursive` option to include the [`finary_api`](https://github.com/lasconic/finary) submodule:
```sh
git clone --recursive https://github.com/YOUR_GITHUB_USERNAME/finalynx.git
# If you forgot --recursive, run: git submodule update --init --recursive
```
2. Install [`poetry`](https://python-poetry.org/) which manages the project dependencies, and get all dependencies needed to work on this project:
```sh
pip3 install poetry && poetry check && poetry install
```
3. Install this project in editable mode so that you don't need to reinstall it on each change:
```sh
pip install -e .
```
4. Try the assistant with:
```sh
python examples/demo.py
```
If you see a template portfolio tree and your investments detected from Finary, then you're now part of the (small) team! 🎉 Now create your own copy of the demo file and go customize it for your own needs (the name `assistant_config` is recommended as it is ignored from git):
```sh
cp examples/demo.py assistant_config.py  # <- Your own portfolio here
```
5. When you're ready to make a contribution, this project uses [`pre-commit`](https://pre-commit.com) to make sure we all use the same code styling and formatting conventions. Make sure to activate it on this repo using:
```sh
pre-commit install --install-hooks
```
6. Now, each time you commit, a list of checks will run on the files you changed. You can try it out before committing with:
```sh
pre-commit run  # optional: --all-files
```

When you commit, make sure to follow the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) naming standard for your commit messages, which will be used to automatically change the release version.

You can now push your changes to your fork (preferably in a separate branch if you plan on contributing again) and create a pull request on the original repo.

### ♻️ Continuous Integration
The original repo has an automated CI/CD pipeline setup for a few tasks:
1. Run the pre-commit checks on any new pull request or push to report if something was forgotten. Also run tests in CI.
2. When something is pushed to the `main` branch (e.g. a merge from your pull request), a job calculates the new version for `finalynx` based on the commit messages, updates the [changelog](https://github.com/MadeInPierre/finalynx/blob/main/CHANGELOG.md), creates a [release](https://github.com/MadeInPierre/finalynx/releases) on GitHub, and publishes the new package to [PyPI](https://pypi.org/project/finalynx/).
3. When a PR is opened or edited, make sure the title and commit messages following the naming convention.

## ❓ Missing stuff for now
Tests and published documentation are limited for now. Ping me if you want me/us to improve them.
