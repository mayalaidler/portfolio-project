#!/bin/bash

# Safety guard: this script hard-resets the git repo — it must only run on the VPS.
if [[ "$(uname)" == "Darwin" ]]; then
    echo "This script is for the VPS only — it hard-resets the repo. Do not run it on your Mac."
    exit 1
fi

VENV=~/portfolio-project/python3-virtualenv

# Navigate to project directory
cd ~/portfolio-project

# Make sure the repo matches the latest main branch on GitHub
git fetch && git reset origin/main --hard

# Create the virtual environment if it doesn't exist, then install dependencies
if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi
source "$VENV/bin/activate"
python -m pip install -r requirements.txt

# Restart the systemd service so it picks up the new code
sudo systemctl restart myportfolio
