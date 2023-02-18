#!/bin/sh

# Clone submodules just in case the user forgot to clone recursively
git submodule update --init --recursive


# Modify finary_api's constants with the full path to prevent relative path issues
FINARY_API_ROOT=$(pwd)/lib/finary_api
CONSTANTS_FILE=$FINARY_API_ROOT/finary_api/constants.py

if ! grep -q finary_assistant "$CONSTANTS_FILE"; then
  echo "\n\n# finary_assistant: Set constants with the full path" >> $CONSTANTS_FILE
  echo "CREDENTIAL_FILE = \"$FINARY_API_ROOT/credentials.json\"" >> $CONSTANTS_FILE
  echo "COOKIE_FILENAME = \"$FINARY_API_ROOT/localCookiesMozilla.txt\"" >> $CONSTANTS_FILE
fi


# Add finary_api to your python path
RCFILE=$HOME/.zshrc
if [ ! -f "$RCFILE" ]; then
    RCFILE=$HOME/.bashrc
fi

if ! grep -q finary_assistant "$RCFILE"; then
    echo "\n\n# finary_assistant: Add finary_api to your python path" >> $RCFILE
    echo "export PYTHONPATH=$FINARY_API_ROOT:\$PYTHONPATH" >> $RCFILE
fi

export PYTHONPATH=$FINARY_API_ROOT:\$PYTHONPATH


# Install dependencies
pip install -r requirements.txt


echo "Finished install!"
