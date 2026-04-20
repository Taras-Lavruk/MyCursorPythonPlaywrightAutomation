# Environment Configuration Guide

This document explains all environment variables used in the project and how they're configured.

## Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your specific values:
   ```bash
   nano .env  # or use your preferred editor
   ```

## Available Environment Variables

### Application URLs

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `BASE_URL` | Base URL for the web application under test | `https://rc-manual.jiraalign.xyz/` | Yes |
| `API_BASE_URL` | Base URL for API testing | `https://rc-manual.jiraalign.xyz/` | Yes |

**Usage:**
- Used in `pages/base_page.py` for navigation
- Used in `tests/api/test_sample_api.py` for API tests
- Used in `conftest.py` for API request context
- Used in `utils/api_client.py` for API calls

### Credentials

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `TEST_USERNAME` | Username for valid login tests | `user@automation.test` | For login tests |
| `TEST_PASSWORD` | Password for valid login tests | `P@ssw0rd` | For login tests |

**Usage:**
- Used in `tests/conftest.py` for the `logged_in_page` fixture
- Used in `tests/e2e/test_login.py` for valid login tests
- Used in `fixtures/users.py` for the `admin_user` fixture

**Security:**
- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore`
- Use different credentials for different environments

### Browser Settings

| Variable | Description | Values | Default |
|----------|-------------|--------|---------|
| `HEADLESS` | Run browser in headless mode | `true`, `false` | `true` |
| `SLOW_MO` | Slow down operations by N milliseconds | Any number (e.g., `500`) | `0` |
| `BROWSER` | Which browser to use | `chromium`, `firefox`, `webkit` | `chromium` |

**Usage:**
- `HEADLESS` - Used in `conftest.py` `browser_type_launch_args` fixture
- `SLOW_MO` - Used in `conftest.py` `browser_type_launch_args` fixture
- `BROWSER` - Used in `Makefile` for `--browser` flag and playwright installation

**Examples:**
```bash
# Run with visible browser
HEADLESS=false pytest tests/e2e/test_login.py

# Run with Firefox
BROWSER=firefox pytest tests/e2e/

# Run with slow motion for debugging
SLOW_MO=1000 pytest tests/e2e/test_login.py
```

### Timeouts

| Variable | Description | Example | Default |
|----------|-------------|---------|---------|
| `DEFAULT_TIMEOUT` | Default timeout for element interactions (ms) | `30000` | `30000` |
| `NAVIGATION_TIMEOUT` | Timeout for page navigation (ms) | `60000` | `60000` |

**Usage:**
- Used in `config/settings.py` and applied in `pages/base_page.py`
- Applied to all page objects via `BasePage.__init__`
- Used in `conftest.py` for context timeout

### Optional Features

| Variable | Description | Values | Default |
|----------|-------------|--------|---------|
| `RECORD_VIDEO` | Enable video recording of test runs | `true`, `1`, or any truthy value | Not set (disabled) |

**Usage:**
- Used in `conftest.py` `browser_context_args` fixture
- Videos are saved to `reports/videos/` when enabled
- Can be enabled via Makefile: `make test-login-video`

## Configuration Files

### config/settings.py

This is the central configuration module that loads all environment variables:

```python
from config.settings import settings

# Access environment variables
settings.BASE_URL
settings.TEST_USERNAME
settings.HEADLESS
settings.DEFAULT_TIMEOUT
```

**Features:**
- Automatically loads `.env` file using `python-dotenv`
- Provides type-safe access to configuration
- Includes sensible defaults for all settings
- Singleton pattern - import once, use anywhere

## Usage Examples

### Running Tests with Different Configurations

```bash
# Development: slow, visible browser
HEADLESS=false SLOW_MO=500 pytest tests/e2e/

# CI/CD: fast, headless
HEADLESS=true pytest tests/e2e/

# Debugging: record video
RECORD_VIDEO=1 pytest tests/e2e/test_login.py

# Different browser
BROWSER=firefox pytest tests/e2e/

# Different environment
BASE_URL=https://staging.example.com pytest tests/e2e/
```

### Using Make Commands

The `Makefile` automatically loads environment variables from `.env`:

```bash
# These commands use settings from .env
make test                    # Uses BASE_URL, BROWSER, etc. from .env
make test-login              # Uses BASE_URL, BROWSER, HEADLESS, etc.
make test-login-headed       # Overrides HEADLESS=false
make test-login-video        # Overrides RECORD_VIDEO=1
```

### Programmatic Access in Tests

```python
from config.settings import settings

def test_example(page):
    # Settings are available throughout the test
    assert settings.BASE_URL is not None
    
    # Conditionally skip tests based on settings
    if not settings.TEST_USERNAME:
        pytest.skip("Valid credentials not configured")
```

## Environment-Specific Configurations

### Local Development

```bash
# .env for local development
BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:8000
TEST_USERNAME=dev@test.com
TEST_PASSWORD=devpass123
HEADLESS=false
SLOW_MO=300
BROWSER=chromium
DEFAULT_TIMEOUT=30000
NAVIGATION_TIMEOUT=60000
```

### CI/CD Environment

For GitHub Actions, GitLab CI, or other CI systems:

1. Do not commit `.env` files
2. Set environment variables in CI configuration:

**GitHub Actions:**
```yaml
env:
  BASE_URL: ${{ secrets.BASE_URL }}
  TEST_USERNAME: ${{ secrets.TEST_USERNAME }}
  TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
  HEADLESS: true
  BROWSER: chromium
```

**GitLab CI:**
```yaml
variables:
  HEADLESS: "true"
  BROWSER: "chromium"
```

### Staging/Production

```bash
# .env.staging
BASE_URL=https://staging.example.com
API_BASE_URL=https://api-staging.example.com
TEST_USERNAME=staging@test.com
TEST_PASSWORD=<staging-password>
HEADLESS=true
BROWSER=chromium
```

## Troubleshooting

### Settings Not Loading

If your settings aren't being used:

1. Verify `.env` exists in project root:
   ```bash
   ls -la .env
   ```

2. Check `.env` syntax (no spaces around `=`):
   ```bash
   # Correct
   BASE_URL=https://example.com
   
   # Incorrect
   BASE_URL = https://example.com
   ```

3. Verify the virtual environment is activated:
   ```bash
   which python
   # Should show: /path/to/project/.venv/bin/python
   ```

### Environment Variables Not Recognized

If pytest doesn't recognize environment variables:

1. Export them before running pytest:
   ```bash
   export HEADLESS=false
   pytest tests/e2e/
   ```

2. Or use inline environment variables:
   ```bash
   HEADLESS=false pytest tests/e2e/
   ```

3. Or use the Makefile which handles this automatically:
   ```bash
   make test-login-headed
   ```

## Best Practices

1. **Never commit `.env`** - It's in `.gitignore` for a reason
2. **Keep `.env.example` updated** - Document all required variables
3. **Use different credentials per environment** - Dev, staging, prod
4. **Document new variables** - Update this file when adding new settings
5. **Validate required settings** - Tests should fail fast if config is missing
6. **Use meaningful defaults** - Settings should work out of the box when possible

## Related Files

- `.env.example` - Template for environment variables
- `.env` - Your local environment variables (not in git)
- `config/settings.py` - Loads and provides access to settings
- `conftest.py` - Uses settings for browser configuration
- `pages/base_page.py` - Uses settings for URLs and timeouts
- `Makefile` - Loads `.env` and passes settings to pytest
