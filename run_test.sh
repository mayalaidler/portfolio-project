#!/bin/bash

if [ -x "$PWD/python3-virtualenv/bin/python" ]; then
    PYTHON="$PWD/python3-virtualenv/bin/python"
elif [ -x "$HOME/python3-virtualenv/bin/python" ]; then
    PYTHON="$HOME/python3-virtualenv/bin/python"
else
    PYTHON="python3"
fi

"$PYTHON" -m unittest discover -v tests/
