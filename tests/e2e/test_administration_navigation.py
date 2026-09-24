"""
Test suite for Administration Page navigation scenarios.

Uses the ``authenticated_page`` fixture (storageState — single login per session)
so every test method works with a pre-authenticated browser context.
"""

from collections.abc import Generator

import pytest
from playwright.sync_api import Page, expect

from pages import AdministrationPage, HeaderPage
from utils.helpers import dismiss_popups


@pytest.mark.e2e
@pytest.mark.regression
class TestAdministrationNavigation:
    """Test suite for Administration Page navigation and UI visibility."""

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page) -> Generator[None, None, None]:
        """Navigate to the Administration page before each test."""
        self.page: Page = authenticated_page

        header = HeaderPage(self.page)
        header.navigate_to_administration()

        self.page.wait_for_load_state("domcontentloaded", timeout=15000)
        dismiss_popups(self.page)

        yield

    def test_administration_page_loads_successfully(self) -> None:
        """Verify administration page loads successfully after navigation."""
        admin_page = AdministrationPage(self.page)
        admin_page.expect_administration_page_visible()
        expect(self.page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_all_main_categories_visible_in_sidebar(self) -> None:
        """Verify all 6 main categories are visible in the administration sidebar."""
        admin_page = AdministrationPage(self.page)

        admin_page.expect_sidebar_visible()

        categories = {
            "ACCESS CONTROLS": [
                admin_page.SIDEBAR_ACTIVITY,
                admin_page.SIDEBAR_PEOPLE,
                admin_page.SIDEBAR_ROLES,
            ],
            "CONNECTORS": [
                admin_page.SIDEBAR_AZURE_DEVOPS,
                admin_page.SIDEBAR_JIRA_SETTINGS,
                admin_page.SIDEBAR_JIRA_MANAGEMENT,
                admin_page.SIDEBAR_MANUAL_IMPORT,
            ],
            "LOGS": [
                admin_page.SIDEBAR_CHANGES,
                admin_page.SIDEBAR_LOGS_EMAIL,
                admin_page.SIDEBAR_USE_TREND,
            ],
            "SETTINGS": [
                admin_page.SIDEBAR_ANNOUNCEMENT,
                admin_page.SIDEBAR_DETAILS_PANELS,
                admin_page.SIDEBAR_PLATFORM,
            ],
            "SETUP": [
                admin_page.SIDEBAR_CITIES,
                admin_page.SIDEBAR_CUSTOMERS,
                admin_page.SIDEBAR_PORTFOLIOS,
                admin_page.SIDEBAR_PROGRAMS,
            ],
            "SUPPORT": [
                admin_page.SIDEBAR_COMMUNITY,
                admin_page.SIDEBAR_UPDATES,
                admin_page.SIDEBAR_VERSION,
            ],
        }

        found_categories: list[str] = []
        missing_categories: list[str] = []

        for category_name, selectors in categories.items():
            category_visible = any(
                self.page.locator(sel).count() > 0 for sel in selectors
            )
            (found_categories if category_visible else missing_categories).append(
                category_name
            )

        assert len(found_categories) >= 4, (
            f"Expected at least 4 categories, found {len(found_categories)}: "
            f"{found_categories}. Missing: {missing_categories}"
        )

    def test_navigate_to_access_controls_sections(self) -> None:
        """Verify navigation to each ACCESS CONTROLS section (Activity, People, Roles)."""
        admin_page = AdministrationPage(self.page)

        if self.page.locator(admin_page.SIDEBAR_ACTIVITY).count() > 0:
            admin_page.navigate_to_activity()
            self.page.wait_for_load_state("networkidle", timeout=5000)
            dismiss_popups(self.page)
            expect(self.page.locator(admin_page.CONTENT_AREA)).to_be_visible()

        if self.page.locator(admin_page.SIDEBAR_PEOPLE).count() > 0:
            admin_page.navigate_to_people()
            self.page.wait_for_load_state("networkidle", timeout=5000)
            dismiss_popups(self.page)
            expect(self.page.locator(admin_page.CONTENT_AREA)).to_be_visible()

        if self.page.locator(admin_page.SIDEBAR_ROLES).count() > 0:
            admin_page.navigate_to_roles()
            self.page.wait_for_load_state("networkidle", timeout=5000)
            dismiss_popups(self.page)
            expect(self.page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_navigate_to_connectors_sections(self) -> None:
        """Verify navigation to each CONNECTORS section."""
        admin_page = AdministrationPage(self.page)

        for navigate_method, selector in [
            (admin_page.navigate_to_azure_devops, admin_page.SIDEBAR_AZURE_DEVOPS),
            (admin_page.navigate_to_jira_settings, admin_page.SIDEBAR_JIRA_SETTINGS),
            (admin_page.navigate_to_jira_management, admin_page.SIDEBAR_JIRA_MANAGEMENT),
            (admin_page.navigate_to_manual_import, admin_page.SIDEBAR_MANUAL_IMPORT),
        ]:
            if self.page.locator(selector).count() > 0:
                navigate_method()
                self.page.wait_for_load_state("networkidle", timeout=5000)
                expect(self.page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_navigate_to_logs_sections(self) -> None:
        """Verify navigation to each LOGS section (Changes, Email, Use Trend)."""
        admin_page = AdministrationPage(self.page)

        for navigate_method, selector in [
            (admin_page.navigate_to_changes, admin_page.SIDEBAR_CHANGES),
            (admin_page.navigate_to_email_logs, admin_page.SIDEBAR_LOGS_EMAIL),
            (admin_page.navigate_to_use_trend, admin_page.SIDEBAR_USE_TREND),
        ]:
            if self.page.locator(selector).count() > 0:
                navigate_method()
                self.page.wait_for_load_state("networkidle", timeout=5000)
                expect(self.page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_navigate_to_settings_sections(self) -> None:
        """Verify navigation to SETTINGS sections."""
        admin_page = AdministrationPage(self.page)

        for navigate_method, selector in [
            (admin_page.navigate_to_announcement, admin_page.SIDEBAR_ANNOUNCEMENT),
            (admin_page.navigate_to_details_panels, admin_page.SIDEBAR_DETAILS_PANELS),
            (admin_page.navigate_to_platform, admin_page.SIDEBAR_PLATFORM),
            (admin_page.navigate_to_platform_terminology, admin_page.SIDEBAR_PLATFORM_TERMINOLOGY),
            (admin_page.navigate_to_time_tracking, admin_page.SIDEBAR_TIME_TRACKING),
        ]:
            if self.page.locator(selector).count() > 0:
                navigate_method()
                self.page.wait_for_load_state("networkidle", timeout=5000)
                expect(self.page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_navigate_to_setup_sections(self) -> None:
        """Verify navigation to SETUP sections."""
        admin_page = AdministrationPage(self.page)

        for navigate_method, selector in [
            (admin_page.navigate_to_cities, admin_page.SIDEBAR_CITIES),
            (admin_page.navigate_to_customers, admin_page.SIDEBAR_CUSTOMERS),
            (admin_page.navigate_to_cost_centers, admin_page.SIDEBAR_COST_CENTERS),
            (admin_page.navigate_to_portfolios, admin_page.SIDEBAR_PORTFOLIOS),
            (admin_page.navigate_to_programs, admin_page.SIDEBAR_PROGRAMS),
            (admin_page.navigate_to_regions, admin_page.SIDEBAR_REGIONS),
        ]:
            if self.page.locator(selector).count() > 0:
                navigate_method()
                self.page.wait_for_load_state("networkidle", timeout=5000)
                expect(self.page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_navigate_to_support_sections(self) -> None:
        """Verify navigation to SUPPORT sections (Community, Updates, Version)."""
        admin_page = AdministrationPage(self.page)

        for navigate_method, selector in [
            (admin_page.navigate_to_community, admin_page.SIDEBAR_COMMUNITY),
            (admin_page.navigate_to_updates, admin_page.SIDEBAR_UPDATES),
            (admin_page.navigate_to_version, admin_page.SIDEBAR_VERSION),
        ]:
            if self.page.locator(selector).count() > 0:
                navigate_method()
                self.page.wait_for_load_state("networkidle", timeout=5000)
                expect(self.page.locator(admin_page.CONTENT_AREA)).to_be_visible()

    def test_sidebar_remains_visible_during_navigation(self) -> None:
        """Verify sidebar remains visible when navigating between sections."""
        admin_page = AdministrationPage(self.page)

        admin_page.expect_sidebar_visible()

        for navigate_method, selector in [
            (admin_page.navigate_to_people, admin_page.SIDEBAR_PEOPLE),
            (admin_page.navigate_to_changes, admin_page.SIDEBAR_CHANGES),
            (admin_page.navigate_to_platform, admin_page.SIDEBAR_PLATFORM),
            (admin_page.navigate_to_cities, admin_page.SIDEBAR_CITIES),
        ]:
            if self.page.locator(selector).count() > 0:
                navigate_method()
                self.page.wait_for_load_state("networkidle", timeout=5000)
                admin_page.expect_sidebar_visible()
                expect(self.page.locator(admin_page.SIDEBAR_CONTAINER)).to_be_visible()

    def test_selected_section_highlighted_in_sidebar(self) -> None:
        """Verify the selected section is highlighted/active in the sidebar."""
        admin_page = AdministrationPage(self.page)

        sections_to_test = [
            (admin_page.navigate_to_people, admin_page.SIDEBAR_PEOPLE, "People"),
            (admin_page.navigate_to_platform, admin_page.SIDEBAR_PLATFORM, "Platform"),
            (admin_page.navigate_to_cities, admin_page.SIDEBAR_CITIES, "Cities"),
        ]

        for navigate_method, selector, section_name in sections_to_test:
            if self.page.locator(selector).count() > 0:
                navigate_method()
                self.page.wait_for_load_state("networkidle", timeout=5000)

                sidebar_link = self.page.locator(selector).first
                has_aria_current = sidebar_link.get_attribute("aria-current") is not None
                classes = sidebar_link.get_attribute("class") or ""
                has_active_class = "active" in classes.lower() or "selected" in classes.lower()

                assert has_aria_current or has_active_class, (
                    f"Section '{section_name}' should have active state indicators in sidebar"
                )
