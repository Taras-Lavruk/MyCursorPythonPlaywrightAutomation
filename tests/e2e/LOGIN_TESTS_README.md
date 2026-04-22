# Login Page Test Suite

## Overview
Comprehensive test suite for the login page functionality covering security, accessibility, user experience, and edge cases.

## Test Coverage

### 1. Basic Functionality Tests
- **test_login_page_loads**: Verifies the login page is accessible
- **test_login_form_elements_visible**: Ensures all form elements render correctly
- **test_valid_login_redirects**: Tests successful authentication flow

### 2. Validation Tests
- **test_login_with_empty_fields_fails**: Tests empty field validation (username only, password only, both empty)
- **test_login_with_invalid_credentials**: Tests various invalid credential scenarios:
  - Wrong credentials
  - Invalid email format
  - Common/weak credentials

### 3. Input Field Tests
- **test_username_field_accepts_input**: Verifies username field accepts text
- **test_password_field_masks_input**: Ensures password field type is "password"
- **test_login_form_clears_on_submission**: Tests form field clearing functionality

### 4. Security Tests
- **test_login_multiple_failed_attempts**: Tests behavior with consecutive failed logins

### 5. User Experience Tests
- **test_submit_button_is_clickable**: Verifies submit button is enabled
- **test_login_form_keyboard_navigation**: Tests Tab and Enter key navigation
- **test_login_page_title_is_set**: Ensures page has a meaningful title

### 6. Accessibility Tests
- **test_login_form_accessibility_labels**: Verifies form inputs have proper labels/placeholders/aria attributes

## Running the Tests

### Run all login tests
```bash
pytest tests/e2e/test_login.py -v
```

### Run specific test class
```bash
pytest tests/e2e/test_login.py::TestLogin -v
```

### Run tests with specific markers
```bash
pytest tests/e2e/test_login.py -m "e2e" -v
pytest tests/e2e/test_login.py -m "regression" -v
```

### Run a specific test
```bash
pytest tests/e2e/test_login.py::TestLogin::test_login_page_loads -v
```

### Run with HTML report
```bash
pytest tests/e2e/test_login.py --html=reports/login_tests.html --self-contained-html
```

### Run in parallel
```bash
pytest tests/e2e/test_login.py -n auto
```

## Configuration Requirements

### Environment Variables (.env file)
```
BASE_URL=https://your-app-url.com/
TEST_USERNAME=valid_user@example.com
TEST_PASSWORD=ValidPassword123
```

### Dependencies
- pytest
- pytest-playwright
- playwright

## Test Markers
- `@pytest.mark.e2e`: End-to-end test
- `@pytest.mark.regression`: Regression test suite
- `@pytest.mark.skipif`: Conditional test execution

## Expected Behavior

### Successful Login
- Valid credentials redirect away from login page
- No error messages displayed

### Failed Login
- User remains on login page
- Error messages may be displayed (if implemented)
- Form data is preserved or cleared (based on implementation)

### Security
- Multiple consecutive failed login attempts are handled
- No sensitive data leaked in error messages

## Future Enhancements
- [ ] Add tests for "Remember Me" functionality (locator defined but not implemented)
- [ ] Add tests for "Forgot Password" link
- [ ] Add tests for password visibility toggle
- [ ] Add tests for rate limiting/account lockout
- [ ] Add tests for SQL injection and XSS attacks
- [ ] Add tests for handling extremely long username/password inputs
- [ ] Add visual regression tests
- [ ] Add performance/load time tests
- [ ] Add tests for "Stay logged in" functionality
- [ ] Add tests for social login (if applicable)
- [ ] Add tests for two-factor authentication (if applicable)

## Notes
- Some tests are parameterized to cover multiple scenarios efficiently
- Failed test screenshots are automatically saved to `reports/screenshots/`
- Tests use Page Object Model pattern for maintainability
- All tests are independent and can run in any order
