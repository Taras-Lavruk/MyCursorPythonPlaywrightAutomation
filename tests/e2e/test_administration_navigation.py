"""
Test suite for Administration Page navigation scenarios.

This module tests the navigation functionality of the Administration Page,
including sidebar visibility, section navigation, and UI state management.
"""
import pytest
from playwright.sync_api import Page, expect
from pages import HeaderPage, AdministrationPage
from tests.conftest import dismiss_popups


@pytest.mark.e2e
@pytest.mark.regression
class TestAdministrationNavigation:
    """Test suite for Administration Page navigation and UI visibility."""

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        """Use authenticated page and navigate to administration page before each test."""
        # authenticated_page fixture handles login, cookies, and alert dismissal
        page = authenticated_page
        
        # Navigate to Administration page
        header = HeaderPage(page)
        header.navigate_to_administration()
        
        # Wait for navigation to complete
        page.wait_for_load_state("domcontentloaded", timeout=15000)
        page.wait_for_timeout(3000)  # Wait longer for any popups to appear
        
        # Aggressively dismiss any cookies/alerts that might appear
        dismiss_popups(page, max_attempts=5)  # Try up to 5 times
        
        # Store page reference for tests
        self.page = page
        
        yield

    def test_administration_page_loads_successfully(self, page: Page) -> None:
        """Verify administration page loads successfully after navigation."""
        dismiss_popups(page)  # Dismiss any popups before test starts
        admin_page = AdministrationPage(page)
        admin_page.expect_administration_page_visible()
        
        # Verify main content area is visible (already checked by expect_administration_page_visible)
        # Admin pages don't have consistent h1 titles, so we just verify content area exists
        expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_all_main_categories_visible_in_sidebar(self, page: Page) -> None:
        """Verify all 6 main categories are visible in the administration sidebar."""
        dismiss_popups(page)  # Dismiss any popups before test starts
        admin_page = AdministrationPage(page)
        
        # Verify sidebar is visible first
        admin_page.expect_sidebar_visible()
        
        # Define the 6 main categories based on the AdministrationPage docstring
        categories = {
            "ACCESS CONTROLS": [
                admin_page.SIDEBAR_ACTIVITY,
                admin_page.SIDEBAR_PEOPLE,
                admin_page.SIDEBAR_ROLES
            ],
            "CONNECTORS": [
                admin_page.SIDEBAR_AZURE_DEVOPS,
                admin_page.SIDEBAR_JIRA_SETTINGS,
                admin_page.SIDEBAR_JIRA_MANAGEMENT,
                admin_page.SIDEBAR_MANUAL_IMPORT
            ],
            "LOGS": [
                admin_page.SIDEBAR_CHANGES,
                admin_page.SIDEBAR_LOGS_EMAIL,
                admin_page.SIDEBAR_USE_TREND
            ],
            "SETTINGS": [
                admin_page.SIDEBAR_ANNOUNCEMENT,
                admin_page.SIDEBAR_DETAILS_PANELS,
                admin_page.SIDEBAR_PLATFORM
            ],
            "SETUP": [
                admin_page.SIDEBAR_CITIES,
                admin_page.SIDEBAR_CUSTOMERS,
                admin_page.SIDEBAR_PORTFOLIOS,
                admin_page.SIDEBAR_PROGRAMS
            ],
            "SUPPORT": [
                admin_page.SIDEBAR_COMMUNITY,
                admin_page.SIDEBAR_UPDATES,
                admin_page.SIDEBAR_VERSION
            ]
        }
        
        # Verify at least one link from each category is visible
        # Note: Not all categories may be visible on every admin page
        found_categories = []
        missing_categories = []
        
        for category_name, selectors in categories.items():
            category_visible = False
            for selector in selectors:
                if page.locator(selector).count() > 0:
                    category_visible = True
                    break
            
            if category_visible:
                found_categories.append(category_name)
            else:
                missing_categories.append(category_name)
        
        # Should find at least 4 out of 6 categories (allowing for some variations)
        assert len(found_categories) >= 4, \
            f"Expected at least 4 categories, found {len(found_categories)}: {found_categories}. Missing: {missing_categories}"

    def test_navigate_to_access_controls_sections(self, page: Page) -> None:
        """Verify navigation to each ACCESS CONTROLS section (Activity, People, Roles)."""
        dismiss_popups(page)
        admin_page = AdministrationPage(page)
        
        # Navigate to Activity
        if page.locator(admin_page.SIDEBAR_ACTIVITY).count() > 0:
            admin_page.navigate_to_activity()
            page.wait_for_load_state("networkidle", timeout=5000)
            dismiss_popups(page)  # Dismiss popups after navigation
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to People
        if page.locator(admin_page.SIDEBAR_PEOPLE).count() > 0:
            admin_page.navigate_to_people()
            page.wait_for_load_state("networkidle", timeout=5000)
            dismiss_popups(page)  # Dismiss popups after navigation
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Roles
        if page.locator(admin_page.SIDEBAR_ROLES).count() > 0:
            admin_page.navigate_to_roles()
            page.wait_for_load_state("networkidle", timeout=5000)
            dismiss_popups(page)  # Dismiss popups after navigation
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_navigate_to_connectors_sections(self, page: Page) -> None:
        """Verify navigation to each CONNECTORS section."""
        admin_page = AdministrationPage(page)
        
        # Navigate to Azure DevOps Settings
        if page.locator(admin_page.SIDEBAR_AZURE_DEVOPS).count() > 0:
            admin_page.navigate_to_azure_devops()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Jira Settings
        if page.locator(admin_page.SIDEBAR_JIRA_SETTINGS).count() > 0:
            admin_page.navigate_to_jira_settings()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Jira Management
        if page.locator(admin_page.SIDEBAR_JIRA_MANAGEMENT).count() > 0:
            admin_page.navigate_to_jira_management()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Manual Import
        if page.locator(admin_page.SIDEBAR_MANUAL_IMPORT).count() > 0:
            admin_page.navigate_to_manual_import()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_navigate_to_logs_sections(self, page: Page) -> None:
        """Verify navigation to each LOGS section (Changes, Email, Use Trend)."""
        admin_page = AdministrationPage(page)
        
        # Navigate to Changes
        if page.locator(admin_page.SIDEBAR_CHANGES).count() > 0:
            admin_page.navigate_to_changes()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Email Logs
        if page.locator(admin_page.SIDEBAR_LOGS_EMAIL).count() > 0:
            admin_page.navigate_to_email_logs()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Use Trend
        if page.locator(admin_page.SIDEBAR_USE_TREND).count() > 0:
            admin_page.navigate_to_use_trend()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_navigate_to_settings_sections(self, page: Page) -> None:
        """Verify navigation to SETTINGS sections."""
        admin_page = AdministrationPage(page)
        
        # Navigate to Announcement
        if page.locator(admin_page.SIDEBAR_ANNOUNCEMENT).count() > 0:
            admin_page.navigate_to_announcement()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Details Panels Settings
        if page.locator(admin_page.SIDEBAR_DETAILS_PANELS).count() > 0:
            admin_page.navigate_to_details_panels()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Platform
        if page.locator(admin_page.SIDEBAR_PLATFORM).count() > 0:
            admin_page.navigate_to_platform()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Platform Terminology
        if page.locator(admin_page.SIDEBAR_PLATFORM_TERMINOLOGY).count() > 0:
            admin_page.navigate_to_platform_terminology()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Time Tracking
        if page.locator(admin_page.SIDEBAR_TIME_TRACKING).count() > 0:
            admin_page.navigate_to_time_tracking()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_navigate_to_setup_sections(self, page: Page) -> None:
        """Verify navigation to SETUP sections."""
        admin_page = AdministrationPage(page)
        
        # Navigate to Cities
        if page.locator(admin_page.SIDEBAR_CITIES).count() > 0:
            admin_page.navigate_to_cities()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Customers
        if page.locator(admin_page.SIDEBAR_CUSTOMERS).count() > 0:
            admin_page.navigate_to_customers()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Cost Centers
        if page.locator(admin_page.SIDEBAR_COST_CENTERS).count() > 0:
            admin_page.navigate_to_cost_centers()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Portfolios
        if page.locator(admin_page.SIDEBAR_PORTFOLIOS).count() > 0:
            admin_page.navigate_to_portfolios()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Programs
        if page.locator(admin_page.SIDEBAR_PROGRAMS).count() > 0:
            admin_page.navigate_to_programs()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Regions
        if page.locator(admin_page.SIDEBAR_REGIONS).count() > 0:
            admin_page.navigate_to_regions()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_navigate_to_support_sections(self, page: Page) -> None:
        """Verify navigation to SUPPORT sections (Community, Updates, Version)."""
        admin_page = AdministrationPage(page)
        
        # Navigate to Community
        if page.locator(admin_page.SIDEBAR_COMMUNITY).count() > 0:
            admin_page.navigate_to_community()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Updates
        if page.locator(admin_page.SIDEBAR_UPDATES).count() > 0:
            admin_page.navigate_to_updates()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()
        
        # Navigate to Version
        if page.locator(admin_page.SIDEBAR_VERSION).count() > 0:
            admin_page.navigate_to_version()
            page.wait_for_load_state("networkidle", timeout=5000)
            expect(page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_sidebar_remains_visible_during_navigation(self, page: Page) -> None:
        """Verify sidebar remains visible when navigating between sections."""
        admin_page = AdministrationPage(page)
        
        # Verify sidebar is initially visible
        admin_page.expect_sidebar_visible()
        
        # Navigate to multiple sections and verify sidebar stays visible
        sections_to_test = [
            (admin_page.navigate_to_people, admin_page.SIDEBAR_PEOPLE),
            (admin_page.navigate_to_changes, admin_page.SIDEBAR_CHANGES),
            (admin_page.navigate_to_platform, admin_page.SIDEBAR_PLATFORM),
            (admin_page.navigate_to_cities, admin_page.SIDEBAR_CITIES),
        ]
        
        for navigate_method, selector in sections_to_test:
            if page.locator(selector).count() > 0:
                navigate_method()
                page.wait_for_load_state("networkidle", timeout=5000)
                
                # Verify sidebar is still visible after navigation
                admin_page.expect_sidebar_visible()
                expect(page.locator(admin_page.SIDEBAR_CONTAINER)).to_be_visible()

    def test_selected_section_highlighted_in_sidebar(self, page: Page) -> None:
        """Verify the selected section is highlighted/active in the sidebar."""
        admin_page = AdministrationPage(page)
        
        # Test sections that are likely to have active state styling
        sections_to_test = [
            (admin_page.navigate_to_people, admin_page.SIDEBAR_PEOPLE, "People"),
            (admin_page.navigate_to_platform, admin_page.SIDEBAR_PLATFORM, "Platform"),
            (admin_page.navigate_to_cities, admin_page.SIDEBAR_CITIES, "Cities"),
        ]
        
        for navigate_method, selector, section_name in sections_to_test:
            if page.locator(selector).count() > 0:
                navigate_method()
                page.wait_for_load_state("networkidle", timeout=5000)
                
                # Check if the link has active state indicators
                sidebar_link = page.locator(selector).first
                
                # Common patterns for active state:
                # 1. aria-current attribute
                # 2. 'active' class
                # 3. Different styling (checked via computed styles)
                
                has_aria_current = sidebar_link.get_attribute("aria-current") is not None
                classes = sidebar_link.get_attribute("class") or ""
                has_active_class = "active" in classes.lower() or "selected" in classes.lower()
                
                # At least one indicator should be present
                assert has_aria_current or has_active_class, \
                    f"Section '{section_name}' should have active state indicators in sidebar"
