#!/bin/sh

# Generate the documentation website (call this script from the repo root!)
pdoc3 . --html
mv html doc/
