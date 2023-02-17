#!/bin/sh

# Small script to ensure quality checks pass before submitting a commit/PR.
python -m black finary_assistant

# Generate the module documentation website in the `gh-pages` branch with:
# ./doc/generate_documentation.sh