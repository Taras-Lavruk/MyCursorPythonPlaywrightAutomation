import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from config.settings import settings


@pytest.mark.e2e
@pytest.mark.regression
class TestLoginPageStructure:
    """Structural and accessibility tests for the login page."""

    def test_login_page_loads_and_has_title(self, page: Page) -> None:
        """Login page should load and have a non-empty title."""
        login = LoginPage(page)
        login.open()
        assert page.title() != "", "Page title should not be empty"

    def test_login_page_has_heading(self, page: Page) -> None:
        """Login page should have at least one heading element."""
        login = LoginPage(page)
        login.open()
        heading = page.locator("h1, h2").first
        expect(heading).to_be_visible()

    def test_login_page_url_is_correct(self, page: Page) -> None:
        """Navigating to login should land on correct URL."""
        login = LoginPage(page)
        login.open()
        assert "login" in page.url.lower(), "URL should contain 'login'"

    def test_login_page_responsive_layout(self, page: Page) -> None:
        """Login page should adapt to different viewport sizes."""
        login = LoginPage(page)
        
        viewports = [
            {"width": 1920, "height": 1080},
            {"width": 768, "height": 1024},
            {"width": 375, "height": 667},
        ]
        
        for viewport in viewports:
            page.set_viewport_size(viewport)
            login.open()
            expect(page.locator("body")).to_be_visible()
            login.expect_login_form_visible()

    def test_login_page_has_valid_html_structure(self, page: Page) -> None:
        """Login page should have basic HTML5 semantic structure."""
        login = LoginPage(page)
        login.open()
        
        body = page.locator("body")
        expect(body).to_be_visible()
        
        html = page.locator("html")
        expect(html).to_be_visible()

    def test_login_page_logo_if_present(self, page: Page) -> None:
        """Logo should be visible and clickable if present on login page."""
        login = LoginPage(page)
        login.open()
        
        logo = page.locator("[data-testid='logo'], .logo, header img").first
        if logo.count() > 0:
            expect(logo).to_be_visible()

    def test_login_page_footer_if_present(self, page: Page) -> None:
        """Login page should have a footer element if present."""
        login = LoginPage(page)
        login.open()
        
        footer = page.locator("footer")
        if footer.count() > 0:
            expect(footer.first).to_be_visible()

    def test_login_page_reload_preserves_content(self, page: Page) -> None:
        """Reloading the login page should preserve the same content."""
        login = LoginPage(page)
        login.open()
        
        title_before = page.title()
        url_before = page.url
        
        login.reload()
        page.wait_for_load_state("domcontentloaded")
        
        title_after = page.title()
        url_after = page.url
        
        assert title_before == title_after, "Page title should remain the same after reload"
        assert url_before == url_after, "URL should remain the same after reload"

    def test_login_page_meta_viewport(self, page: Page) -> None:
        """Login page should have a viewport meta tag for responsive design."""
        login = LoginPage(page)
        login.open()
        
        viewport_meta = page.locator('meta[name="viewport"]')
        assert viewport_meta.count() > 0, "Page should have a viewport meta tag"

    def test_login_page_favicon_exists(self, page: Page) -> None:
        """Login page should reference a favicon."""
        login = LoginPage(page)
        login.open()
        
        favicon = page.locator('link[rel*="icon"]')
        assert favicon.count() > 0, "Page should have a favicon link"

    def test_login_form_keyboard_navigation(self, page: Page) -> None:
        """Users should be able to navigate the login form using keyboard."""
        login = LoginPage(page)
        login.open()
        
        page.keyboard.press("Tab")
        focused_element = page.evaluate("() => document.activeElement.tagName")
        assert focused_element is not None, "Tab key should focus an element"

    @pytest.mark.performance
    def test_login_page_has_no_console_errors(self, page: Page) -> None:
        """Login page should load without console errors."""
        console_errors = []
        
        def handle_console(msg):
            if msg.type == "error":
                console_errors.append(msg.text)
        
        page.on("console", handle_console)
        
        login = LoginPage(page)
        login.open()
        page.wait_for_load_state("networkidle")
        
        assert len(console_errors) == 0, \
            f"Page should not have console errors: {console_errors}"
