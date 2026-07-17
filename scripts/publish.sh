#!/usr/bin/env bash
set -euo pipefail

REPOSITORY_URL="${1:-https://github.com/Nasser934/motion-world.git}"

if [ -d .git ]; then
  echo "This folder is already a Git repository."
  exit 1
fi

git init
git add .
git commit -m "Initial public release of Motion World 0.3.0"
git branch -M main
git remote add origin "$REPOSITORY_URL"
git push -u origin main
