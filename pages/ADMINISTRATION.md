# Administration Page Object Model

## Overview

The `AdministrationPage` class provides methods to interact with the Jira Align Administration interface. This page contains system-wide settings and configurations organized into 6 main categories.

## Access Path

```python
from pages import LoginPage, HomePage, HeaderPage

# Login and navigate to administration
login_page = LoginPage(page)
login_page.open()
login_page.login(username, password)

home_page = HomePage(page)
home_page.click_settings()  # Inherited from HeaderPage

admin_page = AdministrationPage(page)
admin_page.expect_administration_page_visible()
```

## Architecture

- **Parent Class**: `SidebarPage` (which extends `HeaderPage` → `BasePage`)
- **Inherited Features**:
  - Header navigation methods
  - Sidebar collapse/expand functionality
  - Base page utilities (navigate, wait methods)

## Sidebar Structure

The Administration page has 6 main categories with multiple subsections:

### 1. ACCESS CONTROLS
- **Activity** - User activity tracking
- **People** - User management
- **Roles** - Role-based access control

### 2. CONNECTORS
- **Azure DevOps Settings** - Azure DevOps integration configuration
- **Jira Settings** - Jira Cloud/Server connection settings
- **Jira Management** - Manage Jira synchronization
- **Manual Import** - Import data manually

### 3. LOGS
- **Changes** - System change log
- **Email** - Email delivery logs
- **Use Trend** - Usage analytics and trends

### 4. SETTINGS
- **Announcement** - System-wide announcements
- **Details Panels Settings** - Configure details panel display
- **Email** - Email configuration
- **Email Settings** - Advanced email settings
- **Platform** - Platform-wide settings
- **Platform Terminology** - Customize platform terminology
- **Report Baseline** - Report baseline configuration
- **Time Tracking** - Time tracking settings
- **User Record Terminology** - Customize user-facing terminology

### 5. SETUP
- **Cities** - Manage city locations
- **Customers** - Customer management
- **Cost Centers** - Cost center configuration
- **Custom Hierarchies** - Define custom organizational hierarchies
- **Functional Areas** - Functional area setup
- **Organization Structures** - Organization hierarchy
- **Portfolios** - Portfolio management
- **Programs** - Program management
- **Regions** - Geographic regions
- **Theme Groups** - Strategic theme grouping
- **Enterprise Insights** - Enterprise-level insights (NEW)

### 6. SUPPORT
- **Community** - Link to community resources
- **Updates** - System updates and release notes
- **Version** - Current version information

## Usage Examples

### Example 1: Navigate to People Management

```python
from pages import AdministrationPage

admin_page = AdministrationPage(page)

# Navigate to People section
admin_page.navigate_to_people()

# Verify section loaded
admin_page.expect_section_loaded("People")

# Perform actions
admin_page.search_in_section("john.doe@example.com")
count = admin_page.get_table_row_count()
print(f"Found {count} people")
```

### Example 2: Configure Jira Settings

```python
from pages import AdministrationPage

admin_page = AdministrationPage(page)

# Navigate to Jira Settings
admin_page.navigate_to_jira_settings()

# Fill configuration form
admin_page.fill_form_input("Jira URL", "https://your-domain.atlassian.net")
admin_page.fill_form_input("API Token", "your-api-token")

# Save changes
admin_page.save_changes()
admin_page.expect_success_message()
```

### Example 3: Manage Roles

```python
from pages import AdministrationPage

admin_page = AdministrationPage(page)

# Navigate to Roles
admin_page.navigate_to_roles()

# Add new role
admin_page.click_add_button()
admin_page.fill_form_input("Role Name", "Project Viewer")
admin_page.toggle_checkbox("Can View Projects", True)
admin_page.save_modal_form()

# Verify role created
admin_page.expect_success_message()
```

### Example 4: View Change Logs

```python
from pages import AdministrationPage

admin_page = AdministrationPage(page)

# Navigate to Changes log
admin_page.navigate_to_changes()

# Search for specific changes
admin_page.search_in_section("Portfolio")

# Export results
admin_page.export_data()
```

### Example 5: Setup Organization Structure

```python
from pages import AdministrationPage

admin_page = AdministrationPage(page)

# Navigate to Organization Structures
admin_page.navigate_to_organization_structures()

# Add new structure
admin_page.click_add_button()
admin_page.fill_form_input("Structure Name", "North America Division")
admin_page.select_dropdown_option("Parent Structure", "Global")
admin_page.save_modal_form()

# Edit existing structure
admin_page.click_edit_in_row("North America Division")
admin_page.fill_form_input("Description", "North American operations")
admin_page.save_modal_form()
```

## Common Workflows

### Workflow 1: Adding a New Connector

```python
admin_page = AdministrationPage(page)

# 1. Navigate to connector settings
admin_page.navigate_to_azure_devops()

# 2. Open add form
admin_page.click_add_button()

# 3. Fill connector details
admin_page.fill_form_input("Name", "Production ADO")
admin_page.fill_form_input("Organization URL", "https://dev.azure.com/org")
admin_page.fill_form_input("Personal Access Token", "token-value")

# 4. Save
admin_page.save_modal_form()

# 5. Verify
admin_page.expect_success_message()
```

### Workflow 2: Configuring Platform Terminology

```python
admin_page = AdministrationPage(page)

# 1. Navigate to terminology settings
admin_page.navigate_to_platform_terminology()

# 2. Customize terms
admin_page.fill_form_input("Epic", "Initiative")
admin_page.fill_form_input("Story", "User Story")
admin_page.fill_form_input("Feature", "Capability")

# 3. Save changes
admin_page.save_changes()

# 4. Verify
admin_page.expect_success_message()
```

### Workflow 3: Viewing System Information

```python
admin_page = AdministrationPage(page)

# Navigate to version info
admin_page.navigate_to_version()

# Version info is displayed on page
# Can be used for verification in tests
```

## Generic Action Methods

The `AdministrationPage` provides generic methods that work across all sections:

### Table/Grid Operations

```python
# Get row count
count = admin_page.get_table_row_count()

# Search
admin_page.search_in_section("search query")

# Edit row
admin_page.click_edit_in_row("identifier text")

# Delete row
admin_page.click_delete_in_row("identifier text", confirm=True)

# Export data
admin_page.export_data()
```

### Form Operations

```python
# Fill input fields
admin_page.fill_form_input("Field Label", "value")

# Select dropdown
admin_page.select_dropdown_option("Dropdown Label", "option")

# Toggle checkbox
admin_page.toggle_checkbox("Checkbox Label", checked=True)
```

### Modal/Dialog Operations

```python
# Open add form
admin_page.click_add_button()

# Save modal
admin_page.save_modal_form()

# Cancel modal
admin_page.cancel_modal_form()
```

### Common Actions

```python
# Save changes
admin_page.save_changes()

# Cancel changes
admin_page.cancel_changes()

# Reset to defaults
admin_page.reset_to_defaults()

# Confirm action
admin_page.confirm_action()

# Cancel action
admin_page.cancel_action()
```

## Validation Methods

```python
# Verify administration page loaded
admin_page.expect_administration_page_visible()

# Verify specific section loaded
admin_page.expect_section_loaded("Section Name")

# Verify success message
admin_page.expect_success_message()

# Verify error message
admin_page.expect_error_message()

# Check message visibility
if admin_page.is_success_message_visible():
    message = admin_page.get_success_message_text()
    print(f"Success: {message}")

if admin_page.is_error_message_visible():
    error = admin_page.get_error_message_text()
    print(f"Error: {error}")
```

## Best Practices

### 1. Always Verify Page Load

```python
admin_page = AdministrationPage(page)
admin_page.expect_administration_page_visible()  # Wait for page to load
```

### 2. Navigate to Section Before Actions

```python
# Bad - might act on wrong section
admin_page.click_add_button()

# Good - explicit navigation
admin_page.navigate_to_people()
admin_page.click_add_button()
```

### 3. Use Generic Methods When Possible

```python
# Reusable across sections
admin_page.search_in_section("query")
admin_page.get_table_row_count()
```

### 4. Verify Actions with Assertions

```python
admin_page.save_changes()
admin_page.expect_success_message()
assert admin_page.is_success_message_visible()
```

### 5. Handle Confirmations Explicitly

```python
# With confirmation (default)
admin_page.click_delete_in_row("Item Name", confirm=True)

# Without confirmation
admin_page.click_delete_in_row("Item Name", confirm=False)
admin_page.cancel_action()  # Cancel the confirmation dialog
```

## Selectors Strategy

The POM uses flexible, resilient selectors:

```python
# Multiple fallbacks with case-insensitive matching
SIDEBAR_PEOPLE = "a:has-text('People')"

# Generic selectors work across sections
GENERIC_TABLE = "table, [role='grid']"
GENERIC_ADD_BUTTON = "button:has-text('Add'), button:has-text('Create'), button:has-text('New')"
```

## Testing Tips

### Smoke Test Example

```python
def test_administration_sections_accessible(page: Page):
    """Verify all admin sections are accessible."""
    admin_page = AdministrationPage(page)
    
    sections = [
        ("People", admin_page.navigate_to_people),
        ("Roles", admin_page.navigate_to_roles),
        ("Jira Settings", admin_page.navigate_to_jira_settings),
        ("Platform", admin_page.navigate_to_platform),
        ("Portfolios", admin_page.navigate_to_portfolios),
    ]
    
    for section_name, navigate_method in sections:
        navigate_method()
        admin_page.expect_section_loaded(section_name)
```

### Integration Test Example

```python
def test_create_and_delete_role(page: Page):
    """Test role creation and deletion workflow."""
    admin_page = AdministrationPage(page)
    
    # Navigate to roles
    admin_page.navigate_to_roles()
    
    # Create role
    admin_page.click_add_button()
    admin_page.fill_form_input("Role Name", "Test Role")
    admin_page.save_modal_form()
    admin_page.expect_success_message()
    
    # Verify role appears in table
    admin_page.search_in_section("Test Role")
    assert admin_page.get_table_row_count() > 0
    
    # Delete role
    admin_page.click_delete_in_row("Test Role", confirm=True)
    admin_page.expect_success_message()
    
    # Verify role removed
    admin_page.search_in_section("Test Role")
    assert admin_page.get_table_row_count() == 0
```

## Troubleshooting

### Issue: Section Not Loading

```python
# Add explicit wait
admin_page.navigate_to_people()
page.wait_for_load_state("networkidle")
admin_page.expect_section_loaded("People")
```

### Issue: Button Not Clickable

```python
# Ensure element is visible first
button = page.locator(admin_page.GENERIC_ADD_BUTTON).first
button.wait_for(state="visible")
button.click()
```

### Issue: Search Not Working

```python
# Use explicit selector for search in specific section
search_input = page.locator("input[type='search']").first
search_input.fill("query")
search_input.press("Enter")
page.wait_for_timeout(1000)  # Wait for results
```

## Related Pages

- `HeaderPage` - Parent class with header navigation
- `SidebarPage` - Parent class with sidebar methods
- `BasePage` - Root class with core functionality

## Version History

- **v2.0** - Updated to match actual Jira Align structure (April 2026)
  - Replaced generic admin sections with Jira Align specific categories
  - Added 6 main categories: Access Controls, Connectors, Logs, Settings, Setup, Support
  - Added 30+ navigation methods for all subsections
  - Replaced specific action methods with generic reusable methods
  - Updated documentation with real examples
  
- **v1.0** - Initial version with assumed structure
  - Generic admin sections (Users, Teams, Integrations, etc.)
  - Specific CRUD methods for each section
