import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage


@pytest.mark.smoke
@pytest.mark.e2e
class TestHomePage:
    """Smoke tests for the home page."""

    def test_page_loads_and_has_title(self, page: Page) -> None:
        """Home page should load and have a non-empty title."""
        home = HomePage(page)
        home.open()
        assert page.title() != "", "Page title should not be empty"

    def test_page_has_heading(self, page: Page) -> None:
        """Home page should have at least one heading element."""
        home = HomePage(page)
        home.open()
        heading = page.locator("h1, h2").first
        expect(heading).to_be_visible()

    def test_page_url_is_correct(self, page: Page) -> None:
        """Navigating to home should land on BASE_URL."""
        from config.settings import settings
        home = HomePage(page)
        home.open()
        assert settings.BASE_URL in page.url

    @pytest.mark.regression
    def test_page_has_navigation(self, page: Page) -> None:
        """Home page should contain a navigation element."""
        home = HomePage(page)
        home.open()
        nav = page.locator("nav, header").first
        expect(nav).to_be_visible()
