#!/usr/bin/env bash
# Thin wrapper — delegates to check_alignment.py
# Usage: check_alignment.sh <file> [start_line] [end_line] [--fix]
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/check_alignment.py" "$@"
