# Automated Cookie & Alert Banner Handling

## Overview

All tests in this project automatically handle cookie consent and alert banner dismissal. This is implemented through a shared pytest fixture that every test can use.

## What's Automated

### 1. Cookie Consent
- **When**: Before login
- **Where**: Any page that shows a cookie consent banner
- **How**: Automatically clicks "Accept" button if present
- **Implementation**: `BasePage.accept_cookies()` method

### 2. Alert Banner (License Warning)
- **When**: After login
- **What**: Red warning banner about license
- **Where**: Home page after authentication
- **How**: Automatically dismisses if present
- **Implementation**: `HomePage.dismiss_alert_banner()` method

## For Test Developers

### Creating New Tests

Use the `authenticated_page` fixture for any test requiring login:

```python
import pytest
from playwright.sync_api import Page
from pages import HomePage

class TestMyFeature:
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        """Cookies and alerts already handled."""
        self.page = authenticated_page
        yield
    
    def test_my_feature(self, page: Page):
        """Test code here - already authenticated."""
        home = HomePage(page)
        # Your test logic
```

### Benefits

- No need to handle cookies in your tests
- No need to dismiss alert banners
- Clean starting state for every test
- Consistent behavior across all test files

## Implementation Details

### Files Modified

1. **`pages/base_page.py`**
   - Added `accept_cookies()` method
   - Added `is_cookie_banner_visible()` helper
   - Cookie banner locators added

2. **`tests/conftest.py`**
   - Created `authenticated_page` fixture
   - Updated `logged_in_page` fixture
   - Both fixtures handle cookies + alerts automatically

3. **`tests/e2e/test_navigation_example.py`**
   - Updated to use `authenticated_page` fixture
   - Removed duplicate cookie/alert handling code

4. **`tests/e2e/test_administration_navigation.py`**
   - Updated to use `authenticated_page` fixture
   - Removed duplicate cookie/alert handling code

### Rule Created

**`.cursor/rules/test-authentication-pattern.mdc`**
- Documents the authentication pattern
- Provides examples and best practices
- Ensures future tests follow the same pattern

## Architecture

```
┌─────────────────────────────────────────────┐
│           Test Execution Starts             │
└────────────────┬────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────┐
│   authenticated_page fixture (conftest.py)  │
│   1. Open login page                        │
│   2. Accept cookies (if present)            │
│   3. Login with credentials                 │
│   4. Dismiss alert banner (if present)      │
│   5. Return ready page                      │
└────────────────┬────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────┐
│          Your Test Runs Here                │
│   - Clean authenticated state               │
│   - No cookies banner                       │
│   - No alert banner                         │
│   - Ready to test features                  │
└─────────────────────────────────────────────┘
```

## Browser Methods

### BasePage Methods (Available to All Pages)

```python
# Accept cookies if banner is present
page.accept_cookies()

# Check if cookie banner is visible
if page.is_cookie_banner_visible():
    # Handle accordingly
```

### HomePage Methods (Alert Banner)

```python
# Dismiss alert banner if present
home_page.dismiss_alert_banner()

# Get alert message text
message = home_page.get_alert_message()
```

## Testing the Implementation

Run the test suite to verify:

```bash
# Run all E2E tests
pytest tests/e2e/ -v

# Run specific test files
pytest tests/e2e/test_navigation_example.py -v
pytest tests/e2e/test_administration_navigation.py -v
```

## Troubleshooting

### Cookies Not Being Accepted

If cookies aren't being accepted automatically:

1. Check if the cookie banner locator in `BasePage` matches your banner
2. Update `COOKIE_ACCEPT_BUTTON` selector if needed
3. Verify the banner appears before login

### Alert Banner Still Visible

If the alert banner isn't being dismissed:

1. Check if the alert banner locator in `HomePage` is correct
2. Verify the alert appears after login (not before)
3. Check if the close button selector is accurate

### Custom Selectors

Update selectors in:
- `pages/base_page.py` - For cookie banners
- `pages/home_page.py` - For alert banners

## Future Maintenance

All future tests will automatically benefit from this implementation:
- New tests just need to use `authenticated_page` fixture
- Any updates to cookie/alert handling happen in one place
- No code duplication across test files

## Related Documentation

- `.cursor/rules/test-authentication-pattern.mdc` - Complete pattern guide
- `tests/conftest.py` - Fixture implementation
- `pages/base_page.py` - Cookie handling methods
- `pages/home_page.py` - Alert banner methods
