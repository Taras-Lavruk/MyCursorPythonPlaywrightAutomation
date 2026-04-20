#!/bin/bash
# Activate virtual environment for MyPythonPlaywrightAutomation

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/.venv/bin/activate"

echo "✓ Virtual environment activated!"
echo "You can now run pytest commands directly."
echo ""
echo "To deactivate, run: deactivate"
