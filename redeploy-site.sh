#!/bin/bash

if [[ "$(uname)" == "Darwin" ]]; then
    echo "This script is for the VPS only — it hard-resets the repo. Do not run it on your Mac."
    exit 1
fi

cd ~/portfolio-project

git fetch && git reset origin/main --hard

docker compose -f docker-compose.prod.yml down

docker compose -f docker-compose.prod.yml up -d --build
