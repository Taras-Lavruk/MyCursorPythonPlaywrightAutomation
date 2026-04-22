from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for the home / landing page."""

    # Locators
    HEADING = "h1"
    NAV_LINKS = "nav a"
    NAV_ELEMENT = "nav, header nav"
    SEARCH_INPUT = "[data-testid='search-input'], input[type='search'], #search"
    SEARCH_BUTTON = "[data-testid='search-button'], button[type='submit']"
    LOGO = "[data-testid='logo'], .logo, header img"
    FOOTER = "footer"
    MAIN_CONTENT = "main, [role='main'], .main-content"
    CTA_BUTTON = "[data-testid='cta-button'], .cta-button, button.primary"
    LOGIN_LINK = "a[href*='login'], a:has-text('Login'), a:has-text('Sign In')"
    SIGNUP_LINK = "a[href*='signup'], a[href*='register'], a:has-text('Sign Up')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "HomePage":
        self.navigate("/")
        return self

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

    def click_login_link(self) -> None:
        self.page.locator(self.LOGIN_LINK).first.click()

    def click_signup_link(self) -> None:
        self.page.locator(self.SIGNUP_LINK).first.click()

    def click_logo(self) -> None:
        self.page.locator(self.LOGO).first.click()

    def expect_loaded(self) -> None:
        expect(self.page).to_have_title(lambda t: len(t) > 0)
        self.wait_for_load()

    def expect_navigation_visible(self) -> None:
        expect(self.page.locator(self.NAV_ELEMENT).first).to_be_visible()

    def expect_main_content_visible(self) -> None:
        expect(self.page.locator(self.MAIN_CONTENT).first).to_be_visible()

    def expect_footer_visible(self) -> None:
        expect(self.page.locator(self.FOOTER).first).to_be_visible()

    def is_logo_visible(self) -> bool:
        return self.page.locator(self.LOGO).first.is_visible()

    def has_search_feature(self) -> bool:
        return self.page.locator(self.SEARCH_INPUT).count() > 0
