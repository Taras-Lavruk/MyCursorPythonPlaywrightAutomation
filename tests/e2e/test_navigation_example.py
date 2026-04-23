"""
Example tests demonstrating the page object model hierarchy.

These tests show how to use the inherited methods from base classes
and how different pages relate to each other.
"""
import pytest
from playwright.sync_api import Page
from pages import LoginPage, HomePage, EpicGridPage, StoryGridPage


class TestNavigationHierarchy:
    """Test suite demonstrating navigation between pages using the POM hierarchy."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Login before each test and handle cookies + alert banner."""
        login_page = LoginPage(page)
        login_page.open()
        
        # Accept cookies if present
        login_page.accept_cookies()
        
        login_page.login(
            username="user@automation.test",
            password="P@ssw0rd"
        )
        
        # After login, dismiss alert banner if present
        home_page = HomePage(page)
        home_page.wait_for_load()
        if page.locator(home_page.ALERT_BANNER).count() > 0:
            home_page.dismiss_alert_banner()
        
        yield

    def test_alert_banner_on_home_page(self, page: Page):
        """HomePage specific functionality for alert banner."""
        home_page = HomePage(page)
        home_page.expect_home_sections_visible()
        
        # HomePage specific method
        if page.locator(home_page.ALERT_BANNER).count() > 0:
            alert_text = home_page.get_alert_message()
            print(f"Alert: {alert_text}")
            home_page.dismiss_alert_banner()


class TestPageObjectInheritance:
    """Tests that verify inheritance works correctly."""

    def test_epic_page_has_all_parent_methods(self, page: Page):
        """Verify EpicGridPage has methods from all parent classes."""
        epic_page = EpicGridPage(page)
        
        # Has BasePage methods
        assert hasattr(epic_page, 'navigate')
        assert hasattr(epic_page, 'get_url')
        
        # Has HeaderPage methods
        assert hasattr(epic_page, 'click_home')
        assert hasattr(epic_page, 'navigate_to_epics')
        assert hasattr(epic_page, 'click_logout')
        
        # Has SidebarPage methods
        assert hasattr(epic_page, 'is_sidebar_visible')
        assert hasattr(epic_page, 'get_sidebar_links')
        
        # Has GridPage methods
        assert hasattr(epic_page, 'search_grid')
        assert hasattr(epic_page, 'get_row_count')
        
        # Has its own methods
        assert hasattr(epic_page, 'navigate_to_backlog')
        assert hasattr(epic_page, 'quick_add_epic')

    def test_home_page_has_header_but_no_sidebar(self, page: Page):
        """HomePage has header methods but no sidebar (doesn't inherit SidebarPage)."""
        home_page = HomePage(page)
        
        # Has HeaderPage methods
        assert hasattr(home_page, 'click_home')
        assert hasattr(home_page, 'click_logout')
        
        # Does NOT have SidebarPage methods
        assert not hasattr(home_page, 'is_sidebar_visible')
        assert not hasattr(home_page, 'toggle_sidebar')
        
        # Has its own methods
        assert hasattr(home_page, 'is_recent_rooms_visible')
        assert hasattr(home_page, 'get_card_titles')
