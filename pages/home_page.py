from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for the home / landing page."""

    # Locators
    HEADING = "h1"
    NAV_LINKS = "nav a"
    SEARCH_INPUT = "[data-testid='search-input'], input[type='search'], #search"
    SEARCH_BUTTON = "[data-testid='search-button'], button[type='submit']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "HomePage":
        self.navigate("/")
        return self

    def get_heading_text(self) -> str:
        return self.page.locator(self.HEADING).first.inner_text()

    def search(self, query: str) -> None:
        self.page.locator(self.SEARCH_INPUT).fill(query)
        self.page.locator(self.SEARCH_BUTTON).click()

    def get_nav_links(self) -> list[str]:
        return self.page.locator(self.NAV_LINKS).all_inner_texts()

    def expect_loaded(self) -> None:
        expect(self.page).to_have_title(lambda t: len(t) > 0)
        self.wait_for_load()
