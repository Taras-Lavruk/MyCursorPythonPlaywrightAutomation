from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for the authenticated home page (Home tab after login).
    
    Note: This page requires authentication. Users must log in first and will be 
    redirected to this page. Do not navigate directly to this page without logging in.
    """

    # Locators
    HEADING = "h1"
    NAV_LINKS = "nav a"
    NAV_ELEMENT = "nav, header nav"
    HOME_TAB = "[data-testid='home-tab'], a[href*='home'], .home-tab"
    SEARCH_INPUT = "[data-testid='search-input'], input[type='search'], #search"
    SEARCH_BUTTON = "[data-testid='search-button'], button[type='submit']"
    LOGO = "[data-testid='logo'], .logo, header img"
    FOOTER = "footer"
    MAIN_CONTENT = "main, [role='main'], .main-content"
    CTA_BUTTON = "[data-testid='cta-button'], .cta-button, button.primary"
    LOGOUT_LINK = "a[href*='logout'], a:has-text('Logout'), a:has-text('Sign Out')"
    USER_PROFILE = "[data-testid='user-profile'], .user-profile, .user-menu"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def get_heading_text(self) -> str:
        return self.page.locator(self.HEADING).first.inner_text()

    def search(self, query: str) -> None:
        if self.page.locator(self.SEARCH_INPUT).count() > 0:
            self.page.locator(self.SEARCH_INPUT).fill(query)
            if self.page.locator(self.SEARCH_BUTTON).count() > 0:
                self.page.locator(self.SEARCH_BUTTON).click()

    def get_nav_links(self) -> list[str]:
        return self.page.locator(self.NAV_LINKS).all_inner_texts()

    def get_nav_links_count(self) -> int:
        return self.page.locator(self.NAV_LINKS).count()

    def click_home_tab(self) -> None:
        """Click the Home tab to navigate to home page."""
        self.page.locator(self.HOME_TAB).first.click()

    def click_logout(self) -> None:
        """Logout from the authenticated session."""
        self.page.locator(self.LOGOUT_LINK).first.click()

    def click_logo(self) -> None:
        self.page.locator(self.LOGO).first.click()

    def expect_loaded(self) -> None:
        """Verify the home page is loaded after successful login."""
        expect(self.page).to_have_title(lambda t: len(t) > 0)
        self.wait_for_load()

    def expect_navigation_visible(self) -> None:
        expect(self.page.locator(self.NAV_ELEMENT).first).to_be_visible()

    def expect_main_content_visible(self) -> None:
        expect(self.page.locator(self.MAIN_CONTENT).first).to_be_visible()

    def expect_footer_visible(self) -> None:
        expect(self.page.locator(self.FOOTER).first).to_be_visible()

    def expect_user_authenticated(self) -> None:
        """Verify user is authenticated and on the home page."""
        expect(self.page.locator(self.LOGOUT_LINK).first).to_be_visible()
        assert "login" not in self.page.url.lower(), "Should not be on login page"

    def is_logo_visible(self) -> bool:
        return self.page.locator(self.LOGO).first.is_visible()

    def is_user_profile_visible(self) -> bool:
        """Check if user profile/menu is visible (indicates authentication)."""
        return self.page.locator(self.USER_PROFILE).count() > 0 and \
               self.page.locator(self.USER_PROFILE).first.is_visible()

    def has_search_feature(self) -> bool:
        return self.page.locator(self.SEARCH_INPUT).count() > 0
