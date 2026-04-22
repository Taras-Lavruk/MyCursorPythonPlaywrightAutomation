# Login Page Structure Tests

## Overview
Comprehensive structural, accessibility, and performance tests for the login page. These tests complement the functional login tests by focusing on page structure, responsive design, and user experience.

## Test Coverage (12 Tests)

### 1. Basic Structure Tests (3 tests)
- **test_login_page_loads_and_has_title**: Verifies the login page loads with a non-empty title
- **test_login_page_has_heading**: Ensures page has at least one heading element (h1 or h2)
- **test_login_page_url_is_correct**: Confirms navigation to login lands on correct URL

### 2. Performance Tests (1 test)
- **test_login_page_has_no_console_errors**: Checks for JavaScript console errors on load

### 3. Layout & Design Tests (2 tests)
- **test_login_page_responsive_layout**: Tests page adaptation to different viewport sizes:
  - Desktop: 1920x1080
  - Tablet: 768x1024
  - Mobile: 375x667
- **test_login_page_logo_if_present**: Tests logo visibility (if present)

### 4. HTML Structure Tests (3 tests)
- **test_login_page_has_valid_html_structure**: Validates basic HTML5 semantic structure
- **test_login_page_footer_if_present**: Checks for footer element
- **test_login_page_favicon_exists**: Verifies favicon link is present

### 5. Accessibility Tests (2 tests)
- **test_login_page_meta_viewport**: Ensures viewport meta tag exists for responsive design
- **test_login_form_keyboard_navigation**: Tests keyboard navigation with Tab key

### 6. User Experience Tests (1 test)
- **test_login_page_reload_preserves_content**: Ensures content remains consistent after reload

## Running the Tests

### Run all login page structure tests
```bash
pytest tests/e2e/test_login_page_structure.py -v
```

### Run specific test class
```bash
pytest tests/e2e/test_login_page_structure.py::TestLoginPageStructure -v
```

### Run tests with specific markers
```bash
pytest tests/e2e/test_login_page_structure.py -m "e2e" -v
pytest tests/e2e/test_login_page_structure.py -m "regression" -v
pytest tests/e2e/test_login_page_structure.py -m "performance" -v
```

### Run a specific test
```bash
pytest tests/e2e/test_login_page_structure.py::TestLoginPageStructure::test_login_page_loads_and_has_title -v
```

### Run with HTML report
```bash
pytest tests/e2e/test_login_page_structure.py --html=reports/login_structure_tests.html --self-contained-html
```

### Run all login tests (functional + structure)
```bash
pytest tests/e2e/test_login*.py -v
```

## Configuration Requirements

### Environment Variables (.env file)
```
BASE_URL=https://your-app-url.com/
DEFAULT_TIMEOUT=30000
NAVIGATION_TIMEOUT=60000
```

### Dependencies
- pytest
- pytest-playwright
- playwright

## Test Markers
- `@pytest.mark.e2e`: End-to-end test (all 12 tests)
- `@pytest.mark.regression`: Regression test suite (all 12 tests)
- `@pytest.mark.performance`: Performance-related tests (1 test)

## Expected Behavior

### Successful Page Load
- Page loads within configured timeout
- All critical elements are visible
- Login form is rendered properly
- No console errors

### Responsive Design
- Page adapts to different screen sizes
- Login form remains accessible on mobile
- Form elements are readable across all viewports

### Accessibility
- Page has proper viewport meta tag
- Keyboard navigation works
- Form elements can be accessed via Tab key

### Performance
- Page loads without JavaScript errors
- Resources load efficiently

## Relationship with Functional Login Tests

This test suite (`test_login_page_structure.py`) complements the functional login tests (`test_login.py`):

| Aspect | test_login.py | test_login_page_structure.py |
|--------|---------------|------------------------------|
| Focus | Login functionality | Page structure & UX |
| Test Count | 18 (13 methods) | 12 |
| Tests | Form submission, validation, authentication | Layout, accessibility, performance |
| Examples | Empty fields, invalid credentials, valid login | Responsive design, console errors, meta tags |

**Total Login Coverage:** 30 tests (18 functional + 12 structural)

*Note: Functional tests use parameterization, expanding 13 test methods into 18 test cases.*

## Common Test Patterns

### Basic Page Verification
```python
login = LoginPage(page)
login.open()
assert page.title() != ""
```

### Responsive Design Testing
```python
page.set_viewport_size({"width": 375, "height": 667})
login = LoginPage(page)
login.open()
login.expect_login_form_visible()
```

### Console Error Detection
```python
console_errors = []
page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
login.open()
assert len(console_errors) == 0
```

## Future Enhancements
- [ ] Add tests for password visibility toggle (if present)
- [ ] Add tests for social login buttons (if present)
- [ ] Add tests for "Forgot Password" link structure
- [ ] Add visual regression tests using screenshots
- [ ] Add tests for login page animations
- [ ] Add tests for form field auto-focus
- [ ] Add SEO metadata tests (og:tags, twitter:cards)
- [ ] Add tests for ARIA landmark tests
- [ ] Add color contrast tests
- [ ] Add tests for loading states/spinners

## Notes
- Tests use flexible locators to work with various login page implementations
- Some tests gracefully skip if elements are not present (e.g., logo, footer)
- Failed test screenshots are automatically saved to `reports/screenshots/`
- Tests use Page Object Model pattern for maintainability
- All tests are independent and can run in any order
- Console error test uses event listener to capture errors during page load

## Troubleshooting

### Test Failures
- **Page doesn't load**: Check BASE_URL in `.env` and ensure `/login` route exists
- **Timeout errors**: Increase `NAVIGATION_TIMEOUT` or `DEFAULT_TIMEOUT`
- **Element not found**: Verify login page has expected HTML structure
- **Console errors**: Check browser console for actual errors

### Common Issues
1. **Viewport tests fail**: Ensure browser context supports viewport changes
2. **Heading not found**: Update test to match actual heading structure
3. **Favicon test fails**: Check if favicon is properly linked in HTML
4. **Keyboard navigation fails**: Check if login form has focusable elements

## CI/CD Integration

These tests are designed to run in CI/CD pipelines alongside functional tests:
- Fast execution time for quick feedback
- No external dependencies beyond the application
- Comprehensive coverage for confidence in deployments
- Automatic screenshot capture on failures for debugging

## Test Approval

These test scenarios were reviewed and approved according to the Test Scenario Review Workflow:
- ✅ All scenarios presented for user approval
- ✅ Only approved scenarios implemented
- ✅ Tests follow project conventions
- ✅ Documentation maintained with test changes
