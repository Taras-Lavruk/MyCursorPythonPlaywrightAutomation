# Quick Start: Login Page Testing

## Overview
This guide will help you quickly start testing the login page with the comprehensive test suite.

## Prerequisites

1. **Python Environment**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Dependencies Installed**
   ```bash
   make install
   # OR
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Environment Configuration**
   - Copy `.env.example` to `.env`
   - Update with your test credentials:
   ```env
   BASE_URL=https://your-app-url.com/
   TEST_USERNAME=your_test_user@example.com
   TEST_PASSWORD=YourTestPassword123
   ```

## Quick Test Execution

### Method 1: Using Makefile (Recommended)
```bash
# Run all login tests
make test-login

# Run with HTML report
make test-login-report

# Run with visible browser (debugging)
make test-login-headed

# Run security tests only
make test-login-security

# Run in parallel (faster)
make test-login-parallel
```

### Method 2: Using Shell Script
```bash
# Interactive menu
./run_login_tests.sh

# Direct command
./run_login_tests.sh all        # All tests
./run_login_tests.sh report     # With HTML report
./run_login_tests.sh headed     # Visible browser
./run_login_tests.sh security   # Security tests only
```

### Method 3: Direct pytest Commands
```bash
# All login tests
pytest tests/e2e/test_login.py -v

# Specific test
pytest tests/e2e/test_login.py::TestLogin::test_login_page_loads -v

# With markers
pytest -m "e2e and regression" -v

# Generate report
pytest tests/e2e/test_login.py --html=reports/report.html --self-contained-html
```

## Understanding Test Results

### ✅ Passing Test
```
tests/e2e/test_login.py::TestLogin::test_login_page_loads PASSED [100%]
```
- Test executed successfully
- All assertions passed

### ❌ Failing Test
```
tests/e2e/test_login.py::TestLogin::test_valid_login_redirects FAILED [50%]
```
- Check terminal output for assertion errors
- Screenshot saved to `reports/screenshots/`
- Review test logic and application behavior

### ⏭️ Skipped Test
```
tests/e2e/test_login.py::TestLogin::test_valid_login_redirects SKIPPED [50%]
```
- Usually due to missing configuration (e.g., TEST_USERNAME not set)
- Check skip reason in output

## Test Output Artifacts

### Screenshots (on failure)
- Location: `reports/screenshots/`
- Naming: `test_module_test_class_test_name.png`
- Full page screenshots

### Videos (optional)
- Enable: `RECORD_VIDEO=1 pytest ...`
- Location: `reports/videos/`

### HTML Reports
- Generate: `make test-login-report`
- Location: `reports/login_test_report.html`
- Open in browser to view detailed results

## Common Issues & Solutions

### Issue: "TEST_USERNAME not configured"
**Solution**: Ensure `.env` file exists with valid credentials
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Issue: "Timeout waiting for element"
**Solution**: 
- Check if application is running
- Verify BASE_URL in `.env`
- Increase timeout in `config/settings.py`

### Issue: "Browser not found"
**Solution**: Install Playwright browsers
```bash
playwright install chromium
```

### Issue: Tests pass locally but fail in CI
**Solution**:
- Ensure headless mode: `HEADLESS=true`
- Check CI environment has required dependencies
- Verify network access to BASE_URL

## Test Suite Structure

```
tests/e2e/test_login.py          # Main test file
tests/conftest.py                # Test fixtures
pages/login_page.py              # Page Object Model
pages/base_page.py               # Base page class
config/settings.py               # Configuration
.env                             # Environment variables (not committed)
```

## Debugging Failed Tests

### Step 1: Run in Headed Mode
```bash
make test-login-headed
```
Watch the browser to see what's happening

### Step 2: Add Debugging Breakpoint
```python
def test_something(page: Page):
    page.pause()  # Opens Playwright Inspector
    # ... rest of test
```

### Step 3: Increase Verbosity
```bash
pytest tests/e2e/test_login.py -vv -s
```
- `-vv`: Very verbose
- `-s`: Show print statements

### Step 4: Check Screenshot
```bash
open reports/screenshots/
```
Review the screenshot taken at failure

## Best Practices

1. **Run Before Committing**
   ```bash
   make test-login
   ```

2. **Keep Tests Fast**
   - Use `test-login-parallel` for large suites
   - Keep each test under 5 seconds

3. **Isolate Tests**
   - Each test should be independent
   - Don't rely on test execution order

4. **Use Fixtures**
   - Leverage provided fixtures in `conftest.py`
   - Example: `logged_in_page` for authenticated tests

5. **Update Tests with Code**
   - When login page changes, update tests immediately
   - Keep Page Object Model in sync

## Advanced Usage

### Run Specific Test Categories
```bash
# Only smoke tests
pytest tests/e2e/test_login.py -k "test_login_page_loads or test_login_form_elements_visible"

# Only security tests
pytest tests/e2e/test_login.py -k "multiple_failed_attempts"

# Exclude slow tests
pytest tests/e2e/test_login.py -k "not slow"
```

### Custom Test Markers
```python
@pytest.mark.smoke
def test_critical_path(page: Page):
    pass
```

### Retry Failed Tests
```bash
pytest tests/e2e/test_login.py --reruns 3 --reruns-delay 1
```

## Continuous Integration Example

```yaml
# .github/workflows/login-tests.yml
name: Login Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: make install
      - run: make test-login-report
      - uses: actions/upload-artifact@v2
        if: always()
        with:
          name: test-reports
          path: reports/
```

## Next Steps

1. ✅ Run your first test: `make test-login`
2. ✅ Review test coverage: `cat tests/e2e/LOGIN_TEST_MATRIX.md`
3. ✅ Add your custom tests to `test_login.py`
4. ✅ Set up CI/CD pipeline
5. ✅ Monitor test stability and update as needed

## Documentation

- **Test Suite Details**: `tests/e2e/LOGIN_TESTS_README.md`
- **Coverage Matrix**: `tests/e2e/LOGIN_TEST_MATRIX.md`
- **This Guide**: `QUICK_START_LOGIN_TESTS.md`

## Support

For issues or questions:
1. Check test output and screenshots
2. Review documentation
3. Run in headed mode for debugging
4. Check application logs

Happy Testing! 🚀
