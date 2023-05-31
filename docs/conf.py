# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

import finalynx  # noqa: F401, E402


# -- Project information -----------------------------------------------------

project = "Finalynx"
copyright = "2023, Pierre Laclau"
author = "Pierre Laclau"

# The full version, including alpha/beta/rc tags
release = "1.18.1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    # 'sphinx.ext.autosectionlabel',
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "myst_parser",
    # "sphinx_material",
    "sphinx_rtd_theme",
    "autodoc2",  # documentation: https://sphinx-autodoc2.readthedocs.io/en/latest/quickstart.html#using-markdown-myst-docstrings
]

# Parse docstrings with the MyST format, and generate Markdown documentation files.
autodoc2_packages = [
    "../finalynx",
]

# This will render all docstrings as Markdown
autodoc2_docstring_parser_regexes = [
    (r".*", "myst"),
]

# List of modules and objects to skip, e.g. "finary.__meta__"
autodoc2_skip_module_regexes = [
    "finalynx.__meta__",
    "finalynx.__main__",
    "finalynx.usage",
    "finalynx.console",
]
autodoc2_render_plugin = "myst"
myst_enable_extensions = ["fieldlist"]

# Add support for Markdown files
source_suffix = [".rst", ".md"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "sphinx_material"
html_theme = "sphinx_rtd_theme"

# Material theme options (see theme.conf for more information)
# html_theme_options = {
#     # Set the name of the project to appear in the navigation.
#     "nav_title": "Finalynx",
#     # Specify a base_url used to generate sitemap.xml. If not
#     # specified, then no sitemap will be built.
#     # 'base_url': 'https://project.github.io/project',
#     # Set the color and the accent color
#     "color_primary": "blue",
#     "color_accent": "light-blue",
#     # Set the repo location to get a badge with stats
#     "repo_url": "https://github.com/MadeInPierre/finalynx/",
#     "repo_name": "finalynx",
#     # Visible levels of the global TOC; -1 means unlimited
#     "globaltoc_depth": 3,
#     # If False, expand all TOC entries
#     "globaltoc_collapse": False,
#     # If True, show hidden TOC entries
#     "globaltoc_includehidden": False,
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
