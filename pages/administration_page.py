"""
AdministrationPage — Jira Align system-wide settings and configurations.

Access via: HeaderPage.navigate_to_administration()

Sidebar organisation (6 main categories):
  ACCESS CONTROLS : Activity, People, Roles
  CONNECTORS      : Azure DevOps, Jira Settings, Jira Management, Manual Import
  LOGS            : Changes, Email, Use Trend
  SETTINGS        : Announcement, Details Panels, Email, Platform, Terminology, etc.
  SETUP           : Cities, Customers, Cost Centers, Portfolios, Programs, Regions, etc.
  SUPPORT         : Community, Updates, Version
"""

import logging

from playwright.sync_api import Page, expect

from pages.sidebar_page import SidebarPage

_logger = logging.getLogger(__name__)


class AdministrationPage(SidebarPage):
    """Page object for the Jira Align Administration section."""

    # ── Page identity ─────────────────────────────────────────────────────────
    ADMIN_CONTAINER = "#main-content"
    PAGE_TITLE = "h2, h3, .page-title, [class*='admin-header']"
    SECTION_HEADER = "[class*='section-header'], h2, h3"

    # ── ACCESS CONTROLS ───────────────────────────────────────────────────────
    # All sidebar locators are scoped to `aside` to avoid matching header/body links.
    # href-based selectors are preferred; text fallback is used only when href varies.
    SIDEBAR_ACTIVITY = "aside a[href*='Activity' i]"
    SIDEBAR_PEOPLE = "aside a[href*='People' i]"
    SIDEBAR_ROLES = "aside a[href*='RoleSetup' i], aside a[href*='Roles' i]"

    # ── CONNECTORS ────────────────────────────────────────────────────────────
    SIDEBAR_AZURE_DEVOPS = "aside a[href*='AzureDevOps' i]"
    SIDEBAR_JIRA_SETTINGS = "aside a[href*='JiraSettings' i]"
    SIDEBAR_JIRA_MANAGEMENT = "aside a[href*='JiraManagement' i]"
    # href path may omit the query string in some app versions — match by path stem.
    SIDEBAR_MANUAL_IMPORT = "aside a[href*='ManualImportData' i], aside a:has-text('Manual Import')"

    # ── LOGS ──────────────────────────────────────────────────────────────────
    SIDEBAR_CHANGES = "aside a[href*='Changes' i]"
    # Match the path stem only — the query string (?FirstTime=True) is not stable.
    SIDEBAR_LOGS_EMAIL = "aside a[href*='AdminEmailsOutLog' i], aside a:has-text('Email')"
    SIDEBAR_USE_TREND = "aside a[href*='UseTrend' i]"

    # ── SETTINGS ──────────────────────────────────────────────────────────────
    SIDEBAR_ANNOUNCEMENT = "aside a[href*='Announcement' i]"
    SIDEBAR_DETAILS_PANELS = "aside a[href*='DetailsPanels' i]"
    SIDEBAR_EMAIL_SETTINGS = "aside a[href*='MasterEmailSettings' i], aside a[href*='EmailSettings' i]"
    SIDEBAR_PLATFORM = "aside a[href*='Platform' i]"
    SIDEBAR_PLATFORM_TERMINOLOGY = "aside a[href*='PlatformTerminology' i], aside a[href*='Terminology' i]"
    SIDEBAR_REPORT_BASELINE = "aside a[href*='MasterCosting' i], aside a[href*='ReportBaseline' i]"
    SIDEBAR_TIME_TRACKING = "aside a[href*='TimeTracking' i]"
    SIDEBAR_USER_RECORD_TERMINOLOGY = "aside a[href*='UserRecordTerminology' i]"

    # ── SETUP ─────────────────────────────────────────────────────────────────
    SIDEBAR_CITIES = "aside a[href*='Cities' i]"
    SIDEBAR_CUSTOMERS = "aside a[href*='Customers' i]"
    SIDEBAR_COST_CENTERS = "aside a[href*='CostCenters' i]"
    SIDEBAR_CUSTOM_HIERARCHIES = "aside a[href*='Hierarchies' i]"
    SIDEBAR_FUNCTIONAL_AREAS = "aside a[href*='FunctionalAreas' i]"
    SIDEBAR_ORGANIZATION_STRUCTURES = "aside a[href*='Organization' i]"
    SIDEBAR_PORTFOLIOS = "aside a[href*='Portfolios' i]"
    SIDEBAR_PROGRAMS = "aside a[href*='Programs' i]"
    SIDEBAR_REGIONS = "aside a[href*='Regions' i]"
    SIDEBAR_THEME_GROUPS = "aside a[href*='ThemeGroups' i]"
    SIDEBAR_ENTERPRISE_INSIGHTS = "aside a[href*='Insights' i]"

    # ── SUPPORT ───────────────────────────────────────────────────────────────
    SIDEBAR_COMMUNITY = "aside a[href*='Community' i]"
    SIDEBAR_UPDATES = "aside a[href*='Updates' i]"
    SIDEBAR_VERSION = "aside a[href*='MasterVersion' i], aside a[href*='Version' i]"

    # ── Content area ──────────────────────────────────────────────────────────
    CONTENT_AREA = "#main-content"
    SAVE_BUTTON = "button:has-text('Save'), button:has-text('Apply')"
    CANCEL_BUTTON = "button:has-text('Cancel')"
    RESET_BUTTON = "button:has-text('Reset')"

    # ── Generic reusable elements ─────────────────────────────────────────────
    GENERIC_TABLE = "table, [role='grid']"
    GENERIC_ADD_BUTTON = "button:has-text('Add'), button:has-text('Create'), button:has-text('New')"
    GENERIC_SEARCH = "input[type='search'], input[placeholder*='search' i]"
    GENERIC_FILTER = "button:has-text('Filter')"
    GENERIC_EXPORT = "button:has-text('Export')"
    GENERIC_TABLE_ROW = "table tbody tr, [role='row']"
    GENERIC_EDIT_BUTTON = "button[title*='edit' i], a[href*='edit']"
    GENERIC_DELETE_BUTTON = "button[title*='delete' i], button[title*='remove' i]"

    # ── Modals & forms ────────────────────────────────────────────────────────
    GENERIC_MODAL = "[role='dialog'], [class*='modal']"
    GENERIC_MODAL_SAVE = "[role='dialog'] button:has-text('Save'), [role='dialog'] button[type='submit']"
    GENERIC_MODAL_CANCEL = "[role='dialog'] button:has-text('Cancel')"

    # ── Confirmation dialogs ──────────────────────────────────────────────────
    CONFIRM_DIALOG = "[role='alertdialog'], [class*='confirm-dialog']"
    CONFIRM_YES_BUTTON = "button:has-text('Yes'), button:has-text('Confirm'), button:has-text('OK')"
    CONFIRM_NO_BUTTON = "button:has-text('No'), button:has-text('Cancel')"

    # ── Feedback messages ─────────────────────────────────────────────────────
    SUCCESS_MESSAGE = "[class*='success'], [role='alert']:has-text('success')"
    ERROR_MESSAGE = "[class*='error'], [role='alert']:has-text('error')"
    WARNING_MESSAGE = "[class*='warning'], [role='alert']:has-text('warning')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Sidebar navigation — ACCESS CONTROLS ─────────────────────────────────

    def navigate_to_activity(self) -> None:
        """Navigate to the Activity section."""
        self.page.locator(self.SIDEBAR_ACTIVITY).first.click()

    def navigate_to_people(self) -> None:
        """Navigate to People management."""
        self.page.locator(self.SIDEBAR_PEOPLE).first.click()

    def navigate_to_roles(self) -> None:
        """Navigate to Roles."""
        self.page.locator(self.SIDEBAR_ROLES).first.click()

    # ── Sidebar navigation — CONNECTORS ──────────────────────────────────────

    def navigate_to_azure_devops(self) -> None:
        """Navigate to Azure DevOps Settings."""
        self.page.locator(self.SIDEBAR_AZURE_DEVOPS).first.click()

    def navigate_to_jira_settings(self) -> None:
        """Navigate to Jira Settings."""
        self.page.locator(self.SIDEBAR_JIRA_SETTINGS).first.click()

    def navigate_to_jira_management(self) -> None:
        """Navigate to Jira Management."""
        self.page.locator(self.SIDEBAR_JIRA_MANAGEMENT).first.click()

    def navigate_to_manual_import(self) -> None:
        """Navigate to Manual Import."""
        self.page.locator(self.SIDEBAR_MANUAL_IMPORT).click()

    # ── Sidebar navigation — LOGS ─────────────────────────────────────────────

    def navigate_to_changes(self) -> None:
        """Navigate to the Changes log."""
        self.page.locator(self.SIDEBAR_CHANGES).first.click()

    def navigate_to_email_logs(self) -> None:
        """Navigate to the Email logs."""
        self.page.locator(self.SIDEBAR_LOGS_EMAIL).click()

    def navigate_to_use_trend(self) -> None:
        """Navigate to the Use Trend report."""
        self.page.locator(self.SIDEBAR_USE_TREND).first.click()

    # ── Sidebar navigation — SETTINGS ────────────────────────────────────────

    def navigate_to_announcement(self) -> None:
        """Navigate to Announcement settings."""
        self.page.locator(self.SIDEBAR_ANNOUNCEMENT).first.click()

    def navigate_to_details_panels(self) -> None:
        """Navigate to Details Panels settings."""
        self.page.locator(self.SIDEBAR_DETAILS_PANELS).first.click()

    def navigate_to_email_settings(self) -> None:
        """Navigate to Email settings."""
        self.page.locator(self.SIDEBAR_EMAIL_SETTINGS).first.click()

    def navigate_to_platform(self) -> None:
        """Navigate to Platform settings."""
        self.page.locator(self.SIDEBAR_PLATFORM).first.click()

    def navigate_to_platform_terminology(self) -> None:
        """Navigate to Platform Terminology."""
        self.page.locator(self.SIDEBAR_PLATFORM_TERMINOLOGY).first.click()

    def navigate_to_report_baseline(self) -> None:
        """Navigate to Report Baseline."""
        self.page.locator(self.SIDEBAR_REPORT_BASELINE).first.click()

    def navigate_to_time_tracking(self) -> None:
        """Navigate to Time Tracking settings."""
        self.page.locator(self.SIDEBAR_TIME_TRACKING).first.click()

    def navigate_to_user_record_terminology(self) -> None:
        """Navigate to User Record Terminology."""
        self.page.locator(self.SIDEBAR_USER_RECORD_TERMINOLOGY).first.click()

    # ── Sidebar navigation — SETUP ────────────────────────────────────────────

    def navigate_to_cities(self) -> None:
        """Navigate to Cities setup."""
        self.page.locator(self.SIDEBAR_CITIES).first.click()

    def navigate_to_customers(self) -> None:
        """Navigate to Customers setup."""
        self.page.locator(self.SIDEBAR_CUSTOMERS).first.click()

    def navigate_to_cost_centers(self) -> None:
        """Navigate to Cost Centers setup."""
        self.page.locator(self.SIDEBAR_COST_CENTERS).first.click()

    def navigate_to_custom_hierarchies(self) -> None:
        """Navigate to Custom Hierarchies."""
        self.page.locator(self.SIDEBAR_CUSTOM_HIERARCHIES).first.click()

    def navigate_to_functional_areas(self) -> None:
        """Navigate to Functional Areas setup."""
        self.page.locator(self.SIDEBAR_FUNCTIONAL_AREAS).first.click()

    def navigate_to_organization_structures(self) -> None:
        """Navigate to Organization Structures."""
        self.page.locator(self.SIDEBAR_ORGANIZATION_STRUCTURES).first.click()

    def navigate_to_portfolios(self) -> None:
        """Navigate to Portfolios setup."""
        self.page.locator(self.SIDEBAR_PORTFOLIOS).first.click()

    def navigate_to_programs(self) -> None:
        """Navigate to Programs setup."""
        self.page.locator(self.SIDEBAR_PROGRAMS).first.click()

    def navigate_to_regions(self) -> None:
        """Navigate to Regions setup."""
        self.page.locator(self.SIDEBAR_REGIONS).first.click()

    def navigate_to_theme_groups(self) -> None:
        """Navigate to Theme Groups setup."""
        self.page.locator(self.SIDEBAR_THEME_GROUPS).first.click()

    def navigate_to_enterprise_insights(self) -> None:
        """Navigate to Enterprise Insights."""
        self.page.locator(self.SIDEBAR_ENTERPRISE_INSIGHTS).first.click()

    # ── Sidebar navigation — SUPPORT ─────────────────────────────────────────

    def navigate_to_community(self) -> None:
        """Navigate to Community support."""
        self.page.locator(self.SIDEBAR_COMMUNITY).first.click()

    def navigate_to_updates(self) -> None:
        """Navigate to Updates."""
        self.page.locator(self.SIDEBAR_UPDATES).first.click()

    def navigate_to_version(self) -> None:
        """Navigate to Version information."""
        self.page.locator(self.SIDEBAR_VERSION).first.click()

    # ── Generic section actions ───────────────────────────────────────────────

    def click_add_button(self) -> None:
        """Click the Add / Create / New button in the current section."""
        self.page.locator(self.GENERIC_ADD_BUTTON).first.click()

    def search_in_section(self, query: str) -> None:
        """Search within the current admin section."""
        self.page.locator(self.GENERIC_SEARCH).first.fill(query)
        self.page.keyboard.press("Enter")

    def get_table_row_count(self) -> int:
        """Return the number of rows in the current section table."""
        return self.page.locator(self.GENERIC_TABLE_ROW).count()

    def click_edit_in_row(self, row_identifier: str) -> None:
        """Click the edit button in the table row containing row_identifier."""
        row = self.page.locator(f"tr:has-text('{row_identifier}')")
        row.locator(self.GENERIC_EDIT_BUTTON).first.click()

    def click_delete_in_row(self, row_identifier: str, confirm: bool = True) -> None:
        """Click delete in the row matching row_identifier, optionally confirming."""
        row = self.page.locator(f"tr:has-text('{row_identifier}')")
        row.locator(self.GENERIC_DELETE_BUTTON).first.click()
        if confirm:
            self.confirm_action()

    def fill_form_input(self, label_or_placeholder: str, value: str) -> None:
        """Fill a form input identified by its label or placeholder."""
        self.page.locator(
            f"input[placeholder*='{label_or_placeholder}' i], "
            f"input[aria-label*='{label_or_placeholder}' i]"
        ).first.fill(value)

    def select_dropdown_option(self, label: str, option: str) -> None:
        """Select an option from a <select> element identified by aria-label."""
        self.page.locator(f"select[aria-label*='{label}' i]").first.select_option(option)

    def toggle_checkbox(self, label: str, *, checked: bool = True) -> None:
        """Check or uncheck a checkbox identified by its aria-label."""
        cb = self.page.locator(f"input[type='checkbox'][aria-label*='{label}' i]").first
        if checked:
            cb.check()
        else:
            cb.uncheck()

    def save_modal_form(self) -> None:
        """Click the save/submit button in the modal dialog."""
        self.page.locator(self.GENERIC_MODAL_SAVE).first.click()

    def cancel_modal_form(self) -> None:
        """Click the cancel button in the modal dialog."""
        self.page.locator(self.GENERIC_MODAL_CANCEL).first.click()

    def save_changes(self) -> None:
        """Click the Save / Apply button in the current section."""
        self.page.locator(self.SAVE_BUTTON).click()

    def cancel_changes(self) -> None:
        """Click the Cancel button in the current section."""
        self.page.locator(self.CANCEL_BUTTON).click()

    def reset_to_defaults(self) -> None:
        """Click the Reset button in the current section."""
        self.page.locator(self.RESET_BUTTON).click()

    def confirm_action(self) -> None:
        """Confirm an action in the confirmation dialog.

        Clicks are scoped inside the dialog to avoid hitting same-text buttons
        elsewhere on the page (e.g. a form Save button labelled "OK").
        """
        dialog = self.page.locator(self.CONFIRM_DIALOG).first
        if dialog.is_visible(timeout=2000):
            dialog.locator(self.CONFIRM_YES_BUTTON).first.click()

    def cancel_action(self) -> None:
        """Cancel an action in the confirmation dialog."""
        dialog = self.page.locator(self.CONFIRM_DIALOG).first
        if dialog.is_visible(timeout=2000):
            dialog.locator(self.CONFIRM_NO_BUTTON).first.click()

    # ── Assertions ────────────────────────────────────────────────────────────

    def expect_administration_page_visible(self) -> None:
        """Assert the administration page main content is loaded."""
        expect(self.page.locator(self.CONTENT_AREA)).to_be_visible(timeout=10000)
        self.expect_sidebar_visible()

    def expect_section_loaded(self, section_title: str) -> None:
        """Assert a specific section heading is visible."""
        expect(
            self.page.locator(f"{self.SECTION_HEADER}:has-text('{section_title}')")
        ).to_be_visible()

    def expect_success_message(self) -> None:
        """Assert a success message is displayed."""
        expect(self.page.locator(self.SUCCESS_MESSAGE).first).to_be_visible()

    def expect_error_message_visible(self) -> None:
        """Assert an error message is displayed."""
        expect(self.page.locator(self.ERROR_MESSAGE).first).to_be_visible()

    def is_success_message_visible(self) -> bool:
        """Return True if a success message is currently visible."""
        return self.page.locator(self.SUCCESS_MESSAGE).first.is_visible(timeout=0)

    def is_error_message_visible(self) -> bool:
        """Return True if an error message is currently visible."""
        return self.page.locator(self.ERROR_MESSAGE).first.is_visible(timeout=0)

    def get_error_message_text(self) -> str:
        """Return the error message text, or empty string if none is visible."""
        if self.is_error_message_visible():
            return self.page.locator(self.ERROR_MESSAGE).first.inner_text()
        return ""

    def get_success_message_text(self) -> str:
        """Return the success message text, or empty string if none is visible."""
        if self.is_success_message_visible():
            return self.page.locator(self.SUCCESS_MESSAGE).first.inner_text()
        return ""
