#!/usr/bin/env bash
# Atmospheric Physics Sync cron wrapper for Linux / WSL / macOS
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

echo "=== Atmospheric Physics Course Sync Cron ==="
date

python3 scripts/sync_course.py "$@"

echo "=== Finished ==="
