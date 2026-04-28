from playwright.sync_api import Page, expect
from pages.sidebar_page import SidebarPage


class AdministrationPage(SidebarPage):
    """Administration page for Jira Align system-wide settings and configurations.
    
    Accessed via: Header -> SETTINGS_BUTTON (click_settings method in HeaderPage)
    
    The administration sidebar is organized into 6 main categories:
    - ACCESS CONTROLS: Activity, People, Roles
    - CONNECTORS: Azure DevOps, Jira Settings, Jira Management, Manual Import
    - LOGS: Changes, Email, Use Trend
    - SETTINGS: Announcement, Details Panels, Email, Platform, Terminology, etc.
    - SETUP: Cities, Customers, Cost Centers, Portfolios, Programs, Regions, etc.
    - SUPPORT: Community, Updates, Version
    """

    # Page Identifiers
    PAGE_TITLE = "h1:has-text('Administration'), h1:has-text('Settings')"
    ADMIN_CONTAINER = "[class*='admin'], [class*='settings-page']"
    
    # Left Sidebar Navigation - ACCESS CONTROLS Section
    SIDEBAR_ACTIVITY = "a:has-text('Activity')"
    SIDEBAR_PEOPLE = "a:has-text('People')"
    SIDEBAR_ROLES = "a:has-text('Roles')"
    
    # Left Sidebar Navigation - CONNECTORS Section
    SIDEBAR_AZURE_DEVOPS = "a:has-text('Azure DevOps Settings')"
    SIDEBAR_JIRA_SETTINGS = "a:has-text('Jira Settings')"
    SIDEBAR_JIRA_MANAGEMENT = "a:has-text('Jira Management')"
    SIDEBAR_MANUAL_IMPORT = "a:has-text('Manual Import')"
    
    # Left Sidebar Navigation - LOGS Section
    SIDEBAR_CHANGES = "a:has-text('Changes')"
    SIDEBAR_LOGS_EMAIL = "aside a:has-text('Email')"  # More specific to avoid conflict with Settings > Email
    SIDEBAR_USE_TREND = "a:has-text('Use Trend')"
    
    # Left Sidebar Navigation - SETTINGS Section
    SIDEBAR_ANNOUNCEMENT = "a:has-text('Announcement')"
    SIDEBAR_DETAILS_PANELS = "a:has-text('Details Panels Settings')"
    SIDEBAR_EMAIL = "aside a:has-text('Email')"  # First Email link in sidebar
    SIDEBAR_EMAIL_SETTINGS = "a:has-text('Email Settings')"
    SIDEBAR_PLATFORM = "a:has-text('Platform')"
    SIDEBAR_PLATFORM_TERMINOLOGY = "a:has-text('Platform Terminology')"
    SIDEBAR_REPORT_BASELINE = "a:has-text('Report Baseline')"
    SIDEBAR_TIME_TRACKING = "a:has-text('Time Tracking')"
    SIDEBAR_USER_RECORD_TERMINOLOGY = "a:has-text('User Record Terminology')"
    
    # Left Sidebar Navigation - SETUP Section
    SIDEBAR_CITIES = "a:has-text('Cities')"
    SIDEBAR_CUSTOMERS = "a:has-text('Customers')"
    SIDEBAR_COST_CENTERS = "a:has-text('Cost Centers')"
    SIDEBAR_CUSTOM_HIERARCHIES = "a:has-text('Custom Hierarchies')"
    SIDEBAR_FUNCTIONAL_AREAS = "a:has-text('Functional Areas')"
    SIDEBAR_ORGANIZATION_STRUCTURES = "a:has-text('Organization Structures')"
    SIDEBAR_PORTFOLIOS = "a:has-text('Portfolios')"
    SIDEBAR_PROGRAMS = "a:has-text('Programs')"
    SIDEBAR_REGIONS = "a:has-text('Regions')"
    SIDEBAR_THEME_GROUPS = "a:has-text('Theme Groups')"
    SIDEBAR_ENTERPRISE_INSIGHTS = "a:has-text('Enterprise Insights')"
    
    # Left Sidebar Navigation - SUPPORT Section
    SIDEBAR_COMMUNITY = "a:has-text('Community')"
    SIDEBAR_UPDATES = "a:has-text('Updates')"
    SIDEBAR_VERSION = "a:has-text('Version')"
    
    # Content Area - Common Elements
    CONTENT_AREA = "[class*='content'], [class*='admin-panel'], main"
    SECTION_HEADER = "[class*='section-header'], h2, h3"
    SAVE_BUTTON = "button:has-text('Save'), button:has-text('Apply')"
    CANCEL_BUTTON = "button:has-text('Cancel')"
    RESET_BUTTON = "button:has-text('Reset')"
    
    # Generic Content Area Elements - Reusable across all sections
    GENERIC_TABLE = "table, [role='grid']"
    GENERIC_ADD_BUTTON = "button:has-text('Add'), button:has-text('Create'), button:has-text('New')"
    GENERIC_SEARCH = "input[type='search'], input[placeholder*='search' i]"
    GENERIC_FILTER = "button:has-text('Filter')"
    GENERIC_EXPORT = "button:has-text('Export')"
    GENERIC_TABLE_ROW = "table tbody tr, [role='row']"
    GENERIC_EDIT_BUTTON = "button[title*='edit' i], a[href*='edit']"
    GENERIC_DELETE_BUTTON = "button[title*='delete' i], button[title*='remove' i]"
    
    # Generic Modal/Form Elements
    GENERIC_MODAL = "[role='dialog'], [class*='modal']"
    GENERIC_FORM = "form"
    GENERIC_INPUT = "input[type='text']"
    GENERIC_SELECT = "select"
    GENERIC_TEXTAREA = "textarea"
    GENERIC_CHECKBOX = "input[type='checkbox']"
    GENERIC_MODAL_SAVE = "[role='dialog'] button:has-text('Save'), [role='dialog'] button[type='submit']"
    GENERIC_MODAL_CANCEL = "[role='dialog'] button:has-text('Cancel')"
    
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

    # Navigation Methods - ACCESS CONTROLS
    def navigate_to_activity(self) -> None:
        """Navigate to Activity section."""
        self.page.locator(self.SIDEBAR_ACTIVITY).click()

    def navigate_to_people(self) -> None:
        """Navigate to People management section."""
        self.page.locator(self.SIDEBAR_PEOPLE).click()

    def navigate_to_roles(self) -> None:
        """Navigate to Roles section."""
        self.page.locator(self.SIDEBAR_ROLES).click()

    # Navigation Methods - CONNECTORS
    def navigate_to_azure_devops(self) -> None:
        """Navigate to Azure DevOps Settings section."""
        self.page.locator(self.SIDEBAR_AZURE_DEVOPS).click()

    def navigate_to_jira_settings(self) -> None:
        """Navigate to Jira Settings section."""
        self.page.locator(self.SIDEBAR_JIRA_SETTINGS).click()

    def navigate_to_jira_management(self) -> None:
        """Navigate to Jira Management section."""
        self.page.locator(self.SIDEBAR_JIRA_MANAGEMENT).click()

    def navigate_to_manual_import(self) -> None:
        """Navigate to Manual Import section."""
        self.page.locator(self.SIDEBAR_MANUAL_IMPORT).click()

    # Navigation Methods - LOGS
    def navigate_to_changes(self) -> None:
        """Navigate to Changes log section."""
        self.page.locator(self.SIDEBAR_CHANGES).click()

    def navigate_to_email_logs(self) -> None:
        """Navigate to Email logs section."""
        self.page.locator(self.SIDEBAR_LOGS_EMAIL).click()

    def navigate_to_use_trend(self) -> None:
        """Navigate to Use Trend section."""
        self.page.locator(self.SIDEBAR_USE_TREND).click()

    # Navigation Methods - SETTINGS
    def navigate_to_announcement(self) -> None:
        """Navigate to Announcement settings section."""
        self.page.locator(self.SIDEBAR_ANNOUNCEMENT).click()

    def navigate_to_details_panels(self) -> None:
        """Navigate to Details Panels Settings section."""
        self.page.locator(self.SIDEBAR_DETAILS_PANELS).click()

    def navigate_to_email(self) -> None:
        """Navigate to Email settings section."""
        self.page.locator(self.SIDEBAR_EMAIL).click()

    def navigate_to_email_settings(self) -> None:
        """Navigate to Email Settings section."""
        self.page.locator(self.SIDEBAR_EMAIL_SETTINGS).click()

    def navigate_to_platform(self) -> None:
        """Navigate to Platform settings section."""
        self.page.locator(self.SIDEBAR_PLATFORM).click()

    def navigate_to_platform_terminology(self) -> None:
        """Navigate to Platform Terminology section."""
        self.page.locator(self.SIDEBAR_PLATFORM_TERMINOLOGY).click()

    def navigate_to_report_baseline(self) -> None:
        """Navigate to Report Baseline section."""
        self.page.locator(self.SIDEBAR_REPORT_BASELINE).click()

    def navigate_to_time_tracking(self) -> None:
        """Navigate to Time Tracking section."""
        self.page.locator(self.SIDEBAR_TIME_TRACKING).click()

    def navigate_to_user_record_terminology(self) -> None:
        """Navigate to User Record Terminology section."""
        self.page.locator(self.SIDEBAR_USER_RECORD_TERMINOLOGY).click()

    # Navigation Methods - SETUP
    def navigate_to_cities(self) -> None:
        """Navigate to Cities setup section."""
        self.page.locator(self.SIDEBAR_CITIES).click()

    def navigate_to_customers(self) -> None:
        """Navigate to Customers setup section."""
        self.page.locator(self.SIDEBAR_CUSTOMERS).click()

    def navigate_to_cost_centers(self) -> None:
        """Navigate to Cost Centers setup section."""
        self.page.locator(self.SIDEBAR_COST_CENTERS).click()

    def navigate_to_custom_hierarchies(self) -> None:
        """Navigate to Custom Hierarchies section."""
        self.page.locator(self.SIDEBAR_CUSTOM_HIERARCHIES).click()

    def navigate_to_functional_areas(self) -> None:
        """Navigate to Functional Areas setup section."""
        self.page.locator(self.SIDEBAR_FUNCTIONAL_AREAS).click()

    def navigate_to_organization_structures(self) -> None:
        """Navigate to Organization Structures section."""
        self.page.locator(self.SIDEBAR_ORGANIZATION_STRUCTURES).click()

    def navigate_to_portfolios(self) -> None:
        """Navigate to Portfolios setup section."""
        self.page.locator(self.SIDEBAR_PORTFOLIOS).click()

    def navigate_to_programs(self) -> None:
        """Navigate to Programs setup section."""
        self.page.locator(self.SIDEBAR_PROGRAMS).click()

    def navigate_to_regions(self) -> None:
        """Navigate to Regions setup section."""
        self.page.locator(self.SIDEBAR_REGIONS).click()

    def navigate_to_theme_groups(self) -> None:
        """Navigate to Theme Groups setup section."""
        self.page.locator(self.SIDEBAR_THEME_GROUPS).click()

    def navigate_to_enterprise_insights(self) -> None:
        """Navigate to Enterprise Insights section."""
        self.page.locator(self.SIDEBAR_ENTERPRISE_INSIGHTS).click()

    # Navigation Methods - SUPPORT
    def navigate_to_community(self) -> None:
        """Navigate to Community support section."""
        self.page.locator(self.SIDEBAR_COMMUNITY).click()

    def navigate_to_updates(self) -> None:
        """Navigate to Updates section."""
        self.page.locator(self.SIDEBAR_UPDATES).click()

    def navigate_to_version(self) -> None:
        """Navigate to Version information section."""
        self.page.locator(self.SIDEBAR_VERSION).click()

    # Generic Action Methods - Work across different admin sections
    def click_add_button(self) -> None:
        """Click the Add/Create/New button in current section."""
        self.page.locator(self.GENERIC_ADD_BUTTON).first.click()

    def search_in_section(self, query: str) -> None:
        """Search within the current section."""
        search_input = self.page.locator(self.GENERIC_SEARCH).first
        search_input.fill(query)
        self.page.keyboard.press("Enter")

    def get_table_row_count(self) -> int:
        """Get the number of rows in the current table/grid."""
        return self.page.locator(self.GENERIC_TABLE_ROW).count()

    def click_edit_in_row(self, row_identifier: str) -> None:
        """Click edit button in a table row containing specific text."""
        row = self.page.locator(f"tr:has-text('{row_identifier}')")
        row.locator(self.GENERIC_EDIT_BUTTON).first.click()

    def click_delete_in_row(self, row_identifier: str, confirm: bool = True) -> None:
        """Click delete button in a table row and optionally confirm."""
        row = self.page.locator(f"tr:has-text('{row_identifier}')")
        row.locator(self.GENERIC_DELETE_BUTTON).first.click()
        if confirm:
            self.confirm_action()

    def export_data(self) -> None:
        """Click export button in current section."""
        self.page.locator(self.GENERIC_EXPORT).first.click()

    def fill_form_input(self, label_or_placeholder: str, value: str) -> None:
        """Fill a form input by its label or placeholder text."""
        input_field = self.page.locator(
            f"input[placeholder*='{label_or_placeholder}' i], "
            f"input[aria-label*='{label_or_placeholder}' i]"
        ).first
        input_field.fill(value)

    def select_dropdown_option(self, label: str, option: str) -> None:
        """Select an option from a dropdown."""
        dropdown = self.page.locator(f"select[aria-label*='{label}' i]").first
        dropdown.select_option(option)

    def toggle_checkbox(self, label: str, checked: bool = True) -> None:
        """Toggle a checkbox by its label."""
        checkbox = self.page.locator(
            f"input[type='checkbox'][aria-label*='{label}' i]"
        ).first
        if checked:
            checkbox.check()
        else:
            checkbox.uncheck()

    def save_modal_form(self) -> None:
        """Click save/submit button in modal dialog."""
        self.page.locator(self.GENERIC_MODAL_SAVE).first.click()

    def cancel_modal_form(self) -> None:
        """Click cancel button in modal dialog."""
        self.page.locator(self.GENERIC_MODAL_CANCEL).first.click()

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
