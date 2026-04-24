# Administration Page Object Model (POM)

## Overview

The `AdministrationPage` class provides a comprehensive Page Object Model for interacting with the Jira Align Administration interface. It extends `SidebarPage`, inheriting header navigation and sidebar functionality.

## Access Path

```
Header -> SETTINGS_BUTTON -> Administration Page
```

## Architecture

```
BasePage
    └── HeaderPage (header navigation)
        └── SidebarPage (sidebar navigation)
            └── AdministrationPage (admin-specific elements)
```

## File Location

```
pages/administration_page.py
```

## Key Features

### 1. Navigation Sections

The Administration page contains multiple sections accessible via the left sidebar:

- **General Settings** - Company name, timezone, date format, language
- **Users** - User management and access control
- **Teams** - Team organization and structure
- **Roles & Permissions** - Role-based access control
- **Integrations** - Third-party integration management
- **Connectors** - External system connectors (Jira, Azure DevOps, etc.)
- **Custom Fields** - Custom field configuration
- **Workflows** - Workflow design and management
- **Email** - SMTP configuration
- **Notifications** - Notification preferences
- **Security** - Security policies (MFA, SSO, password policy)
- **Audit Log** - System activity tracking
- **System** - System information and maintenance
- **Licensing** - License management
- **API** - API key management

### 2. Common Patterns

#### Navigation Pattern

```python
from pages.header_page import HeaderPage
from pages.administration_page import AdministrationPage

# Navigate to Administration
header = HeaderPage(page)
admin = AdministrationPage(page)

header.click_settings()
admin.expect_administration_page_visible()

# Navigate to specific section
admin.navigate_to_users()
admin.expect_section_loaded("Users")
```

#### CRUD Operations Pattern

Most sections follow this pattern:

1. **List View** - Table or grid with search/filter
2. **Add Button** - Opens form/modal for creation
3. **Row Actions** - Edit, delete, activate/deactivate
4. **Form** - Input fields with save/cancel buttons

## Usage Examples

### Example 1: User Management

```python
def test_create_user(page: Page) -> None:
    header = HeaderPage(page)
    admin = AdministrationPage(page)
    
    # Navigate to Administration > Users
    header.click_settings()
    admin.navigate_to_users()
    
    # Create a new user
    admin.create_user(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        role="Standard User"
    )
    
    # Verify success
    admin.expect_success_message()
    
    # Search for the new user
    admin.search_users("john.doe@example.com")
    assert admin.get_users_count() > 0
```

### Example 2: Search and Filter

```python
def test_search_users(page: Page) -> None:
    header = HeaderPage(page)
    admin = AdministrationPage(page)
    
    header.click_settings()
    admin.navigate_to_users()
    
    # Search for users
    admin.search_users("developer")
    
    # Verify results
    assert admin.get_users_count() > 0
```

### Example 3: Integration Configuration

```python
def test_enable_integration(page: Page) -> None:
    header = HeaderPage(page)
    admin = AdministrationPage(page)
    
    header.click_settings()
    admin.navigate_to_integrations()
    
    # Enable specific integration
    admin.enable_integration("Slack")
    
    # Configure it
    admin.configure_integration("Slack")
    
    # Test connection
    admin.test_integration("Slack")
    
    admin.expect_success_message()
```

### Example 4: Security Settings

```python
def test_configure_security(page: Page) -> None:
    header = HeaderPage(page)
    admin = AdministrationPage(page)
    
    header.click_settings()
    admin.navigate_to_security()
    
    # Enable security features
    admin.enable_mfa()
    admin.set_session_timeout("30")
    
    # Save changes
    admin.save_changes()
    admin.expect_success_message()
```

### Example 5: Audit Log Search

```python
def test_audit_log_search(page: Page) -> None:
    header = HeaderPage(page)
    admin = AdministrationPage(page)
    
    header.click_settings()
    admin.navigate_to_audit_log()
    
    # Filter by date range
    admin.filter_audit_log_by_date(
        from_date="2024-01-01",
        to_date="2024-12-31"
    )
    
    # Search for specific actions
    admin.search_audit_log("user created")
    
    # Export results
    admin.export_audit_log()
```

### Example 6: API Key Management

```python
def test_create_api_key(page: Page) -> None:
    header = HeaderPage(page)
    admin = AdministrationPage(page)
    
    header.click_settings()
    admin.navigate_to_api()
    
    # Generate new API key
    api_key = admin.create_api_key("CI/CD Pipeline")
    
    # Verify key was created
    assert api_key, "API key should be generated"
    
    # Store key securely (in real test, you'd save this)
    print(f"Generated API Key: {api_key}")
```

## Selector Strategy

The page uses flexible, resilient selectors:

1. **Text-based selectors** - Prioritized for stability
2. **Attribute-based selectors** - For form inputs and buttons
3. **Fallback selectors** - Multiple selector options using `,` separator

### Example Selector

```python
SETTINGS_BUTTON = "button[aria-label*='setting' i], header button[title*='setting' i]"
```

This selector:
- Looks for `aria-label` containing "setting" (case-insensitive)
- Falls back to `title` attribute in header
- Works across different implementations

## Validation Methods

### Page-Level Validation

```python
admin.expect_administration_page_visible()  # Verifies page loaded
admin.expect_sidebar_visible()              # Verifies sidebar present
admin.expect_section_loaded("Users")        # Verifies section loaded
```

### Message Validation

```python
admin.expect_success_message()              # Assert success message shown
admin.expect_error_message()                # Assert error message shown
admin.is_success_message_visible()          # Check if success message visible
admin.get_success_message_text()            # Get success message text
```

## Common Workflows

### 1. User CRUD Workflow

```python
# Create
admin.navigate_to_users()
admin.create_user("Jane", "Smith", "jane@example.com", "Admin")
admin.expect_success_message()

# Read/Search
admin.search_users("jane@example.com")
assert admin.get_users_count() > 0

# Update
admin.edit_user_by_email("jane@example.com")
# ... modify fields ...
admin.save_changes()

# Delete
admin.delete_user_by_email("jane@example.com", confirm=True)
admin.expect_success_message()
```

### 2. Integration Testing Workflow

```python
admin.navigate_to_integrations()
admin.click_add_integration()
# ... configure integration ...
admin.test_integration("Integration Name")
admin.expect_success_message()
```

### 3. Connector Configuration Workflow

```python
admin.navigate_to_connectors()
admin.click_add_connector()
admin.configure_connector(
    connector_type="Jira Cloud",
    url="https://your-domain.atlassian.net",
    username="api@example.com",
    password="api_token_here"
)
admin.save_changes()
admin.expect_success_message()
```

## Test Markers

The test suite uses pytest markers for organization:

- `@pytest.mark.authenticated` - Requires authenticated session
- `@pytest.mark.admin_required` - Requires admin privileges
- `@pytest.mark.skip(reason="...")` - Skips destructive tests

### Example

```python
@pytest.mark.authenticated
@pytest.mark.admin_required
class TestUserManagement:
    def test_user_list_visible(self, page: Page) -> None:
        # Test implementation
        pass
```

## Best Practices

### 1. Always Verify Navigation

```python
header.click_settings()
admin.expect_administration_page_visible()  # ✓ Verify page loaded
```

### 2. Use Waiting Strategies

```python
# For search/filter operations
admin.search_users("query")
page.wait_for_timeout(1000)  # Wait for results to load
users_count = admin.get_users_count()
```

### 3. Handle Confirmations

```python
# With confirmation
admin.delete_user_by_email("user@example.com", confirm=True)

# Without confirmation (for testing cancel behavior)
admin.delete_user_by_email("user@example.com", confirm=False)
admin.cancel_action()
```

### 4. Validate Success/Error States

```python
admin.create_user(...)

if admin.is_success_message_visible():
    print(admin.get_success_message_text())
elif admin.is_error_message_visible():
    print(admin.get_error_message_text())
```

### 5. Clean Up Test Data

```python
@pytest.fixture
def test_user(page: Page):
    """Create a test user and clean up after."""
    admin = AdministrationPage(page)
    test_email = f"test.{uuid.uuid4()}@example.com"
    
    admin.navigate_to_users()
    admin.create_user("Test", "User", test_email, "Standard User")
    
    yield test_email
    
    # Cleanup
    admin.delete_user_by_email(test_email, confirm=True)
```

## Extending the POM

### Adding New Sections

If the Administration page has additional sections:

1. Add sidebar selector:
```python
SIDEBAR_NEW_SECTION = "a:has-text('New Section')"
```

2. Add navigation method:
```python
def navigate_to_new_section(self) -> None:
    """Navigate to New Section."""
    self.page.locator(self.SIDEBAR_NEW_SECTION).click()
```

3. Add section-specific selectors and methods.

### Adding New Actions

For new functionality within existing sections:

1. Add element selectors
2. Add action methods
3. Add validation methods

## Troubleshooting

### Issue: Page not loading

```python
# Add explicit wait
admin.expect_administration_page_visible()
page.wait_for_load_state("networkidle")
```

### Issue: Element not found

```python
# Check if element exists before interacting
if page.locator(admin.USERS_ADD_BUTTON).count() > 0:
    admin.click_add_user()
else:
    print("Add User button not found - may be permission issue")
```

### Issue: Test data cleanup

```python
# Always use fixtures for test data
@pytest.fixture(autouse=True)
def cleanup(page: Page):
    yield
    # Cleanup code runs after each test
    admin = AdministrationPage(page)
    admin.navigate_to_users()
    # Delete test users created during test
```

## Related Pages

- `base_page.py` - Base functionality for all pages
- `header_page.py` - Header navigation (inherited)
- `sidebar_page.py` - Sidebar navigation (inherited)
- `grid_page.py` - Similar grid operations pattern

## Test Files

- `tests/e2e/test_administration.py` - Comprehensive test suite
- `tests/e2e/test_navigation_example.py` - General navigation patterns

## Future Enhancements

1. **Dynamic Section Detection** - Auto-detect available sections
2. **Bulk Operations** - Batch user/team operations
3. **Export/Import** - Configuration export/import
4. **Advanced Filtering** - Complex filter combinations
5. **Permission Checking** - Automatic permission validation
