#!/bin/bash

# Kill all existing tmux sessions
tmux kill-server 2>/dev/null || true

# Navigate to project directory
cd ~/portfolio-project

# Pull latest changes from main branch
git fetch && git reset origin/main --hard

# Enter virtual environment and install dependencies
source ~/python3-virtualenv/bin/activate
pip install -r requirements.txt

# Start a new detached tmux session that runs the Flask server
tmux new-session -d -s flask -c ~/portfolio-project \
  'source ~/python3-virtualenv/bin/activate && FLASK_ENV=production flask run --host=0.0.0.0'
