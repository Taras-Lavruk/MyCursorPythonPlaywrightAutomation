# Python Playwright Test Automation

A pytest + Playwright test automation framework following the Page Object Model pattern, with support for E2E and API testing.

## Project Structure

```
.
├── config/              # Environment settings (loaded from .env)
├── fixtures/            # Shared pytest fixtures and test data factories
├── pages/               # Page Object Models
│   ├── base_page.py     # Base class for all page objects
│   ├── home_page.py
│   └── login_page.py
├── tests/
│   ├── e2e/             # Browser-based end-to-end tests
│   └── api/             # API-level tests (no browser)
├── utils/               # Helpers, API client, data generators
├── reports/             # Generated HTML reports + screenshots (git-ignored)
├── .github/workflows/   # GitHub Actions CI pipeline
├── conftest.py          # Root fixtures (browser, context, page, hooks)
├── pyproject.toml       # pytest configuration and markers
└── requirements.txt     # Python dependencies
```

## Quick Start

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# OR use the provided activation script:
source activate.sh          # macOS/Linux
# .venv\Scripts\activate    # Windows
```

### 2. Install dependencies

**Option A: Using Make (recommended)**
```bash
make install
```

**Option B: Using pip directly**
```bash
# Make sure virtual environment is activated first!
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your BASE_URL, credentials, etc.
```

See [ENVIRONMENT.md](ENVIRONMENT.md) for detailed documentation on all available environment variables and how they're used.

### 4. Run tests

**Using Make commands (works without activating venv)**
```bash
# View all available commands
make help

# Run all tests
make test

# Run login tests
make test-login

# Run login tests with visible browser
make test-login-headed

# Run login tests with HTML report
make test-login-report

# Run tests in parallel
make test-login-parallel
```

**Using pytest directly (requires activated venv)**
```bash
# IMPORTANT: Activate virtual environment first!
source .venv/bin/activate   # or: source activate.sh

# Run all tests
pytest

# Run only smoke tests
pytest -m smoke

# Run only E2E tests
pytest tests/e2e/

# Run only API tests
pytest tests/api/

# Run in headed mode (see the browser)
HEADLESS=false pytest

# Run in parallel (requires pytest-xdist)
pytest -n auto

# Re-run failed tests up to 2 times
pytest --reruns 2
```

**Note:** If you see "pytest not found", you need to either:
- Use `make` commands (they automatically use the virtual environment), or
- Activate the virtual environment: `source .venv/bin/activate`

## Markers

| Marker       | Description                          |
|--------------|--------------------------------------|
| `smoke`      | Quick sanity checks                  |
| `regression` | Full regression suite                |
| `e2e`        | Browser-based end-to-end tests       |
| `api`        | API-level tests (no browser)         |
| `slow`       | Tests that take longer than usual    |

## Reports

After a test run, open `reports/report.html` in your browser.
Screenshots of failed tests are saved to `reports/screenshots/`.

## Adding a New Page Object

1. Create `pages/my_page.py` inheriting from `BasePage`.
2. Define locator constants and action methods.
3. Export it from `pages/__init__.py`.

## CI / CD

The GitHub Actions workflow in `.github/workflows/playwright.yml` runs smoke tests on every push/PR and the full suite on a daily schedule.
Store secrets (`BASE_URL`, `TEST_USERNAME`, `TEST_PASSWORD`) in your repository's **Settings → Secrets**.
