# Troubleshooting Guide

## "pytest not found" Error

If you see `pytest not found` or `command not found: pytest` in your terminal:

### Solution 1: Use Make Commands (Easiest)
The Make commands automatically use the virtual environment, so you don't need to activate it:

```bash
make test-login
make test
make test-login-headed
```

View all available commands:
```bash
make help
```

### Solution 2: Activate Virtual Environment
If you want to run pytest commands directly:

```bash
# Option A: Use the activation script
source activate.sh

# Option B: Activate manually
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

After activation, you should see `(.venv)` in your terminal prompt:
```
(.venv) username@computer MyPythonPlaywrightAutomation %
```

Now you can run pytest directly:
```bash
pytest tests/e2e/test_login.py -v
```

### Solution 3: Use Full Path to pytest
Without activating the virtual environment, you can use the full path:

```bash
.venv/bin/pytest tests/e2e/test_login.py -v
```

## Virtual Environment Not Found

If you get errors about the virtual environment not existing:

```bash
# Create the virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

## Other Common Issues

### Browser Not Installed
Error: `Executable doesn't exist at ...`

Solution:
```bash
# Make sure virtual environment is activated
source .venv/bin/activate
playwright install chromium
```

### Missing Dependencies
Error: `ModuleNotFoundError: No module named 'pytest'`

Solution:
```bash
# Make sure virtual environment is activated
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables Not Set
Error: Tests fail because URLs or credentials are missing

Solution:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
nano .env  # or use any text editor
```

## Verifying Your Setup

Run these commands to verify everything is set up correctly:

```bash
# Activate virtual environment
source .venv/bin/activate

# Check Python version
python --version

# Check pytest is installed
pytest --version

# Check playwright is installed
playwright --version

# Deactivate when done
deactivate
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `source .venv/bin/activate` | Activate virtual environment |
| `deactivate` | Deactivate virtual environment |
| `which pytest` | Check if pytest is in PATH |
| `make help` | Show all available make commands |
| `.venv/bin/pytest --version` | Check pytest version without activation |
