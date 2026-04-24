from playwright.sync_api import Page, expect
from pages.sidebar_page import SidebarPage


class AdministrationPage(SidebarPage):
    """Administration page for system-wide settings and configurations.
    
    Accessed via Header -> SETTINGS_BUTTON
    Contains left sidebar navigation for different admin sections.
    """

    # Page Identifiers
    PAGE_TITLE = "h1:has-text('Administration'), h1:has-text('Settings')"
    ADMIN_CONTAINER = "[class*='admin'], [class*='settings-page']"
    
    # Left Sidebar Navigation - Admin Sections
    SIDEBAR_GENERAL = "a:has-text('General')"
    SIDEBAR_USERS = "a:has-text('Users')"
    SIDEBAR_TEAMS = "a:has-text('Teams')"
    SIDEBAR_ROLES = "a:has-text('Roles'), a:has-text('Permissions')"
    SIDEBAR_INTEGRATIONS = "a:has-text('Integrations')"
    SIDEBAR_CONNECTORS = "a:has-text('Connectors')"
    SIDEBAR_CUSTOM_FIELDS = "a:has-text('Custom Fields')"
    SIDEBAR_WORKFLOWS = "a:has-text('Workflows')"
    SIDEBAR_EMAIL = "a:has-text('Email')"
    SIDEBAR_NOTIFICATIONS = "a:has-text('Notifications')"
    SIDEBAR_SECURITY = "a:has-text('Security')"
    SIDEBAR_AUDIT_LOG = "a:has-text('Audit Log')"
    SIDEBAR_SYSTEM = "a:has-text('System')"
    SIDEBAR_LICENSING = "a:has-text('Licensing'), a:has-text('License')"
    SIDEBAR_BACKUP = "a:has-text('Backup')"
    SIDEBAR_API = "a:has-text('API')"
    
    # Content Area - Common Elements
    CONTENT_AREA = "[class*='content'], [class*='admin-panel'], main"
    SECTION_HEADER = "[class*='section-header'], h2, h3"
    SAVE_BUTTON = "button:has-text('Save'), button:has-text('Apply')"
    CANCEL_BUTTON = "button:has-text('Cancel')"
    RESET_BUTTON = "button:has-text('Reset')"
    
    # General Settings Section
    GENERAL_COMPANY_NAME = "input[name*='company' i], input[placeholder*='company' i]"
    GENERAL_TIMEZONE = "select[name*='timezone' i], select[placeholder*='timezone' i]"
    GENERAL_DATE_FORMAT = "select[name*='date' i], select[placeholder*='format' i]"
    GENERAL_LANGUAGE = "select[name*='language' i], select[placeholder*='language' i]"
    
    # Users Section
    USERS_TABLE = "table, [role='grid']"
    USERS_ADD_BUTTON = "button:has-text('Add User'), button:has-text('Create User')"
    USERS_SEARCH = "input[type='search'], input[placeholder*='search' i]"
    USERS_FILTER = "button:has-text('Filter')"
    USERS_EXPORT = "button:has-text('Export')"
    USERS_ROW = "table tbody tr, [role='row']"
    USERS_EMAIL_COLUMN = "td[data-column*='email' i], td:nth-child(2)"
    USERS_ROLE_COLUMN = "td[data-column*='role' i], td:nth-child(3)"
    USERS_STATUS_COLUMN = "td[data-column*='status' i], td:nth-child(4)"
    USERS_ACTIONS_COLUMN = "td[data-column*='action' i], td:last-child"
    
    # User Actions (Row-level)
    USER_EDIT_BUTTON = "button[title*='edit' i], a[href*='edit']"
    USER_DELETE_BUTTON = "button[title*='delete' i], button[title*='remove' i]"
    USER_ACTIVATE_BUTTON = "button:has-text('Activate')"
    USER_DEACTIVATE_BUTTON = "button:has-text('Deactivate')"
    
    # Add/Edit User Modal/Form
    USER_MODAL = "[role='dialog'], [class*='modal']"
    USER_FORM = "form, [class*='user-form']"
    USER_FIRST_NAME = "input[name*='first' i], input[placeholder*='first' i]"
    USER_LAST_NAME = "input[name*='last' i], input[placeholder*='last' i]"
    USER_EMAIL = "input[name*='email' i], input[type='email']"
    USER_ROLE = "select[name*='role' i], select[placeholder*='role' i]"
    USER_TEAM = "select[name*='team' i], select[placeholder*='team' i]"
    USER_STATUS = "select[name*='status' i]"
    USER_SAVE_BUTTON = "[role='dialog'] button:has-text('Save'), form button[type='submit']"
    USER_CANCEL_BUTTON = "[role='dialog'] button:has-text('Cancel')"
    
    # Teams Section
    TEAMS_TABLE = "table, [role='grid']"
    TEAMS_ADD_BUTTON = "button:has-text('Add Team'), button:has-text('Create Team')"
    TEAMS_SEARCH = "input[type='search'], input[placeholder*='search' i]"
    TEAMS_ROW = "table tbody tr, [role='row']"
    
    # Roles & Permissions Section
    ROLES_TABLE = "table, [role='grid']"
    ROLES_ADD_BUTTON = "button:has-text('Add Role'), button:has-text('Create Role')"
    ROLES_SEARCH = "input[type='search'], input[placeholder*='search' i]"
    PERMISSIONS_GRID = "[class*='permissions'], [class*='capabilities']"
    PERMISSION_CHECKBOX = "input[type='checkbox']"
    
    # Integrations Section
    INTEGRATIONS_LIST = "[class*='integration'], [class*='connector']"
    INTEGRATIONS_ADD_BUTTON = "button:has-text('Add Integration'), button:has-text('Configure')"
    INTEGRATION_CARD = "[class*='card'], [class*='integration-item']"
    INTEGRATION_ENABLE_TOGGLE = "input[type='checkbox'], button[role='switch']"
    INTEGRATION_CONFIGURE_BUTTON = "button:has-text('Configure'), button:has-text('Settings')"
    INTEGRATION_TEST_BUTTON = "button:has-text('Test Connection')"
    
    # Connectors Section (Jira, Azure DevOps, etc.)
    CONNECTORS_TABLE = "table, [role='grid']"
    CONNECTORS_ADD_BUTTON = "button:has-text('Add Connector'), button:has-text('New Connector')"
    CONNECTOR_TYPE_SELECT = "select[name*='type' i], select[placeholder*='type' i]"
    CONNECTOR_URL = "input[name*='url' i], input[placeholder*='url' i]"
    CONNECTOR_USERNAME = "input[name*='username' i], input[placeholder*='username' i]"
    CONNECTOR_PASSWORD = "input[type='password']"
    CONNECTOR_TOKEN = "input[name*='token' i], input[placeholder*='token' i]"
    
    # Custom Fields Section
    CUSTOM_FIELDS_TABLE = "table, [role='grid']"
    CUSTOM_FIELDS_ADD_BUTTON = "button:has-text('Add Field'), button:has-text('Create Field')"
    CUSTOM_FIELD_NAME = "input[name*='name' i], input[placeholder*='name' i]"
    CUSTOM_FIELD_TYPE = "select[name*='type' i], select[placeholder*='type' i]"
    CUSTOM_FIELD_ENTITY = "select[name*='entity' i], select[placeholder*='entity' i]"
    
    # Workflows Section
    WORKFLOWS_TABLE = "table, [role='grid']"
    WORKFLOWS_ADD_BUTTON = "button:has-text('Add Workflow'), button:has-text('Create Workflow')"
    WORKFLOW_NAME = "input[name*='workflow' i], input[placeholder*='workflow' i]"
    WORKFLOW_CANVAS = "[class*='workflow-designer'], [class*='canvas']"
    
    # Email Configuration Section
    EMAIL_SMTP_HOST = "input[name*='smtp' i], input[placeholder*='host' i]"
    EMAIL_SMTP_PORT = "input[name*='port' i], input[type='number']"
    EMAIL_USERNAME = "input[name*='username' i], input[placeholder*='username' i]"
    EMAIL_PASSWORD = "input[type='password']"
    EMAIL_FROM_ADDRESS = "input[name*='from' i], input[type='email']"
    EMAIL_TEST_BUTTON = "button:has-text('Test Email'), button:has-text('Send Test')"
    
    # Security Section
    SECURITY_PASSWORD_POLICY = "[class*='password-policy']"
    SECURITY_SESSION_TIMEOUT = "input[name*='session' i], input[name*='timeout' i]"
    SECURITY_MFA_ENABLE = "input[type='checkbox'][name*='mfa' i]"
    SECURITY_SSO_ENABLE = "input[type='checkbox'][name*='sso' i]"
    SECURITY_IP_WHITELIST = "textarea[name*='whitelist' i], textarea[placeholder*='ip' i]"
    
    # Audit Log Section
    AUDIT_LOG_TABLE = "table, [role='grid']"
    AUDIT_LOG_SEARCH = "input[type='search'], input[placeholder*='search' i]"
    AUDIT_LOG_DATE_FROM = "input[type='date'][name*='from' i]"
    AUDIT_LOG_DATE_TO = "input[type='date'][name*='to' i]"
    AUDIT_LOG_USER_FILTER = "select[name*='user' i], input[placeholder*='user' i]"
    AUDIT_LOG_ACTION_FILTER = "select[name*='action' i], select[placeholder*='event' i]"
    AUDIT_LOG_EXPORT = "button:has-text('Export')"
    
    # System Section
    SYSTEM_VERSION = "[class*='version'], p:has-text('Version')"
    SYSTEM_STATUS = "[class*='status'], [class*='health']"
    SYSTEM_MAINTENANCE_MODE = "input[type='checkbox'][name*='maintenance' i]"
    SYSTEM_CLEAR_CACHE = "button:has-text('Clear Cache')"
    SYSTEM_RESTART = "button:has-text('Restart')"
    
    # Licensing Section
    LICENSE_KEY = "input[name*='license' i], textarea[name*='license' i]"
    LICENSE_STATUS = "[class*='license-status']"
    LICENSE_EXPIRY = "[class*='expiry'], p:has-text('Expires')"
    LICENSE_USERS_COUNT = "[class*='users'], p:has-text('Users')"
    LICENSE_UPLOAD_BUTTON = "button:has-text('Upload License')"
    LICENSE_VALIDATE_BUTTON = "button:has-text('Validate')"
    
    # API Section
    API_KEYS_TABLE = "table, [role='grid']"
    API_ADD_KEY_BUTTON = "button:has-text('Generate Key'), button:has-text('Create Key')"
    API_KEY_NAME = "input[name*='name' i], input[placeholder*='name' i]"
    API_KEY_VALUE = "input[readonly], code, [class*='api-key']"
    API_KEY_REVOKE = "button:has-text('Revoke')"
    API_DOCUMENTATION_LINK = "a:has-text('API Documentation')"
    
    # Confirmation Dialogs
    CONFIRM_DIALOG = "[role='alertdialog'], [class*='confirm-dialog']"
    CONFIRM_YES_BUTTON = "button:has-text('Yes'), button:has-text('Confirm'), button:has-text('OK')"
    CONFIRM_NO_BUTTON = "button:has-text('No'), button:has-text('Cancel')"
    
    # Toast/Alert Messages
    SUCCESS_MESSAGE = "[class*='success'], [role='alert']:has-text('success')"
    ERROR_MESSAGE = "[class*='error'], [role='alert']:has-text('error')"
    WARNING_MESSAGE = "[class*='warning'], [role='alert']:has-text('warning')"
    INFO_MESSAGE = "[class*='info'], [role='alert']:has-text('info')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Navigation Methods
    def navigate_to_general(self) -> None:
        """Navigate to General Settings section."""
        self.page.locator(self.SIDEBAR_GENERAL).click()

    def navigate_to_users(self) -> None:
        """Navigate to Users management section."""
        self.page.locator(self.SIDEBAR_USERS).click()

    def navigate_to_teams(self) -> None:
        """Navigate to Teams management section."""
        self.page.locator(self.SIDEBAR_TEAMS).click()

    def navigate_to_roles(self) -> None:
        """Navigate to Roles & Permissions section."""
        self.page.locator(self.SIDEBAR_ROLES).click()

    def navigate_to_integrations(self) -> None:
        """Navigate to Integrations section."""
        self.page.locator(self.SIDEBAR_INTEGRATIONS).click()

    def navigate_to_connectors(self) -> None:
        """Navigate to Connectors section."""
        self.page.locator(self.SIDEBAR_CONNECTORS).click()

    def navigate_to_custom_fields(self) -> None:
        """Navigate to Custom Fields section."""
        self.page.locator(self.SIDEBAR_CUSTOM_FIELDS).click()

    def navigate_to_workflows(self) -> None:
        """Navigate to Workflows section."""
        self.page.locator(self.SIDEBAR_WORKFLOWS).click()

    def navigate_to_email(self) -> None:
        """Navigate to Email configuration section."""
        self.page.locator(self.SIDEBAR_EMAIL).click()

    def navigate_to_notifications(self) -> None:
        """Navigate to Notifications section."""
        self.page.locator(self.SIDEBAR_NOTIFICATIONS).click()

    def navigate_to_security(self) -> None:
        """Navigate to Security settings section."""
        self.page.locator(self.SIDEBAR_SECURITY).click()

    def navigate_to_audit_log(self) -> None:
        """Navigate to Audit Log section."""
        self.page.locator(self.SIDEBAR_AUDIT_LOG).click()

    def navigate_to_system(self) -> None:
        """Navigate to System settings section."""
        self.page.locator(self.SIDEBAR_SYSTEM).click()

    def navigate_to_licensing(self) -> None:
        """Navigate to Licensing section."""
        self.page.locator(self.SIDEBAR_LICENSING).click()

    def navigate_to_api(self) -> None:
        """Navigate to API management section."""
        self.page.locator(self.SIDEBAR_API).click()

    # General Settings Actions
    def set_company_name(self, name: str) -> None:
        """Set company name in General settings."""
        self.page.locator(self.GENERAL_COMPANY_NAME).fill(name)

    def set_timezone(self, timezone: str) -> None:
        """Set system timezone."""
        self.page.locator(self.GENERAL_TIMEZONE).select_option(timezone)

    def set_date_format(self, format: str) -> None:
        """Set date format."""
        self.page.locator(self.GENERAL_DATE_FORMAT).select_option(format)

    # User Management Actions
    def click_add_user(self) -> None:
        """Open Add User form/modal."""
        self.page.locator(self.USERS_ADD_BUTTON).click()

    def search_users(self, query: str) -> None:
        """Search for users by name or email."""
        self.page.locator(self.USERS_SEARCH).fill(query)
        self.page.keyboard.press("Enter")

    def get_users_count(self) -> int:
        """Get the number of users in the table."""
        return self.page.locator(self.USERS_ROW).count()

    def create_user(self, first_name: str, last_name: str, email: str, role: str) -> None:
        """Create a new user with basic information."""
        self.click_add_user()
        self.page.locator(self.USER_FIRST_NAME).fill(first_name)
        self.page.locator(self.USER_LAST_NAME).fill(last_name)
        self.page.locator(self.USER_EMAIL).fill(email)
        self.page.locator(self.USER_ROLE).select_option(role)
        self.page.locator(self.USER_SAVE_BUTTON).click()

    def edit_user_by_email(self, email: str) -> None:
        """Click edit button for a user with specific email."""
        row = self.page.locator(f"tr:has-text('{email}')")
        row.locator(self.USER_EDIT_BUTTON).click()

    def delete_user_by_email(self, email: str, confirm: bool = True) -> None:
        """Delete a user by email with optional confirmation."""
        row = self.page.locator(f"tr:has-text('{email}')")
        row.locator(self.USER_DELETE_BUTTON).click()
        if confirm:
            self.confirm_action()

    # Team Management Actions
    def click_add_team(self) -> None:
        """Open Add Team form/modal."""
        self.page.locator(self.TEAMS_ADD_BUTTON).click()

    def search_teams(self, query: str) -> None:
        """Search for teams by name."""
        self.page.locator(self.TEAMS_SEARCH).fill(query)
        self.page.keyboard.press("Enter")

    def get_teams_count(self) -> int:
        """Get the number of teams in the table."""
        return self.page.locator(self.TEAMS_ROW).count()

    # Role Management Actions
    def click_add_role(self) -> None:
        """Open Add Role form/modal."""
        self.page.locator(self.ROLES_ADD_BUTTON).click()

    def search_roles(self, query: str) -> None:
        """Search for roles by name."""
        self.page.locator(self.ROLES_SEARCH).fill(query)
        self.page.keyboard.press("Enter")

    # Integration Actions
    def click_add_integration(self) -> None:
        """Open Add Integration form/modal."""
        self.page.locator(self.INTEGRATIONS_ADD_BUTTON).click()

    def enable_integration(self, integration_name: str) -> None:
        """Enable an integration by name."""
        card = self.page.locator(f"{self.INTEGRATION_CARD}:has-text('{integration_name}')")
        card.locator(self.INTEGRATION_ENABLE_TOGGLE).check()

    def configure_integration(self, integration_name: str) -> None:
        """Open configuration for specific integration."""
        card = self.page.locator(f"{self.INTEGRATION_CARD}:has-text('{integration_name}')")
        card.locator(self.INTEGRATION_CONFIGURE_BUTTON).click()

    def test_integration(self, integration_name: str) -> None:
        """Test connection for specific integration."""
        card = self.page.locator(f"{self.INTEGRATION_CARD}:has-text('{integration_name}')")
        card.locator(self.INTEGRATION_TEST_BUTTON).click()

    # Connector Actions
    def click_add_connector(self) -> None:
        """Open Add Connector form/modal."""
        self.page.locator(self.CONNECTORS_ADD_BUTTON).click()

    def configure_connector(self, connector_type: str, url: str, username: str, password: str) -> None:
        """Configure a new connector with credentials."""
        self.page.locator(self.CONNECTOR_TYPE_SELECT).select_option(connector_type)
        self.page.locator(self.CONNECTOR_URL).fill(url)
        self.page.locator(self.CONNECTOR_USERNAME).fill(username)
        self.page.locator(self.CONNECTOR_PASSWORD).fill(password)

    # Custom Fields Actions
    def click_add_custom_field(self) -> None:
        """Open Add Custom Field form/modal."""
        self.page.locator(self.CUSTOM_FIELDS_ADD_BUTTON).click()

    def create_custom_field(self, name: str, field_type: str, entity: str) -> None:
        """Create a new custom field."""
        self.click_add_custom_field()
        self.page.locator(self.CUSTOM_FIELD_NAME).fill(name)
        self.page.locator(self.CUSTOM_FIELD_TYPE).select_option(field_type)
        self.page.locator(self.CUSTOM_FIELD_ENTITY).select_option(entity)
        self.page.locator(self.SAVE_BUTTON).click()

    # Email Configuration Actions
    def configure_smtp(self, host: str, port: str, username: str, password: str, from_address: str) -> None:
        """Configure SMTP email settings."""
        self.page.locator(self.EMAIL_SMTP_HOST).fill(host)
        self.page.locator(self.EMAIL_SMTP_PORT).fill(port)
        self.page.locator(self.EMAIL_USERNAME).fill(username)
        self.page.locator(self.EMAIL_PASSWORD).fill(password)
        self.page.locator(self.EMAIL_FROM_ADDRESS).fill(from_address)

    def test_email_configuration(self) -> None:
        """Send test email to verify configuration."""
        self.page.locator(self.EMAIL_TEST_BUTTON).click()

    # Security Actions
    def enable_mfa(self) -> None:
        """Enable multi-factor authentication."""
        self.page.locator(self.SECURITY_MFA_ENABLE).check()

    def enable_sso(self) -> None:
        """Enable single sign-on."""
        self.page.locator(self.SECURITY_SSO_ENABLE).check()

    def set_session_timeout(self, minutes: str) -> None:
        """Set session timeout in minutes."""
        self.page.locator(self.SECURITY_SESSION_TIMEOUT).fill(minutes)

    # Audit Log Actions
    def search_audit_log(self, query: str) -> None:
        """Search audit log entries."""
        self.page.locator(self.AUDIT_LOG_SEARCH).fill(query)
        self.page.keyboard.press("Enter")

    def filter_audit_log_by_date(self, from_date: str, to_date: str) -> None:
        """Filter audit log by date range."""
        self.page.locator(self.AUDIT_LOG_DATE_FROM).fill(from_date)
        self.page.locator(self.AUDIT_LOG_DATE_TO).fill(to_date)

    def export_audit_log(self) -> None:
        """Export audit log to file."""
        self.page.locator(self.AUDIT_LOG_EXPORT).click()

    # System Actions
    def clear_cache(self) -> None:
        """Clear system cache."""
        self.page.locator(self.SYSTEM_CLEAR_CACHE).click()

    def enable_maintenance_mode(self) -> None:
        """Enable maintenance mode."""
        self.page.locator(self.SYSTEM_MAINTENANCE_MODE).check()

    def get_system_version(self) -> str:
        """Get system version."""
        return self.page.locator(self.SYSTEM_VERSION).inner_text()

    # Licensing Actions
    def upload_license(self, license_key: str) -> None:
        """Upload/paste license key."""
        self.page.locator(self.LICENSE_KEY).fill(license_key)
        self.page.locator(self.LICENSE_VALIDATE_BUTTON).click()

    def get_license_status(self) -> str:
        """Get license status."""
        return self.page.locator(self.LICENSE_STATUS).inner_text()

    # API Management Actions
    def click_generate_api_key(self) -> None:
        """Open Generate API Key form/modal."""
        self.page.locator(self.API_ADD_KEY_BUTTON).click()

    def create_api_key(self, name: str) -> str:
        """Create a new API key and return its value."""
        self.click_generate_api_key()
        self.page.locator(self.API_KEY_NAME).fill(name)
        self.page.locator(self.SAVE_BUTTON).click()
        return self.page.locator(self.API_KEY_VALUE).inner_text()

    def revoke_api_key(self, key_name: str, confirm: bool = True) -> None:
        """Revoke an API key by name."""
        row = self.page.locator(f"tr:has-text('{key_name}')")
        row.locator(self.API_KEY_REVOKE).click()
        if confirm:
            self.confirm_action()

    # Common Actions
    def save_changes(self) -> None:
        """Save changes in current section."""
        self.page.locator(self.SAVE_BUTTON).click()

    def cancel_changes(self) -> None:
        """Cancel changes in current section."""
        self.page.locator(self.CANCEL_BUTTON).click()

    def reset_to_defaults(self) -> None:
        """Reset settings to default values."""
        self.page.locator(self.RESET_BUTTON).click()

    def confirm_action(self) -> None:
        """Confirm action in confirmation dialog."""
        if self.page.locator(self.CONFIRM_DIALOG).count() > 0:
            self.page.locator(self.CONFIRM_YES_BUTTON).click()

    def cancel_action(self) -> None:
        """Cancel action in confirmation dialog."""
        if self.page.locator(self.CONFIRM_DIALOG).count() > 0:
            self.page.locator(self.CONFIRM_NO_BUTTON).click()

    # Validation Methods
    def expect_administration_page_visible(self) -> None:
        """Verify the administration page is loaded."""
        expect(self.page.locator(self.PAGE_TITLE).first).to_be_visible(timeout=10000)
        self.expect_sidebar_visible()

    def expect_section_loaded(self, section_title: str) -> None:
        """Verify a specific section is loaded."""
        expect(self.page.locator(f"{self.SECTION_HEADER}:has-text('{section_title}')")).to_be_visible()

    def expect_success_message(self) -> None:
        """Verify success message is displayed."""
        expect(self.page.locator(self.SUCCESS_MESSAGE).first).to_be_visible()

    def expect_error_message(self) -> None:
        """Verify error message is displayed."""
        expect(self.page.locator(self.ERROR_MESSAGE).first).to_be_visible()

    def is_success_message_visible(self) -> bool:
        """Check if success message is visible."""
        return self.page.locator(self.SUCCESS_MESSAGE).count() > 0 and \
               self.page.locator(self.SUCCESS_MESSAGE).first.is_visible()

    def is_error_message_visible(self) -> bool:
        """Check if error message is visible."""
        return self.page.locator(self.ERROR_MESSAGE).count() > 0 and \
               self.page.locator(self.ERROR_MESSAGE).first.is_visible()

    def get_error_message_text(self) -> str:
        """Get error message text."""
        if self.is_error_message_visible():
            return self.page.locator(self.ERROR_MESSAGE).first.inner_text()
        return ""

    def get_success_message_text(self) -> str:
        """Get success message text."""
        if self.is_success_message_visible():
            return self.page.locator(self.SUCCESS_MESSAGE).first.inner_text()
        return ""
