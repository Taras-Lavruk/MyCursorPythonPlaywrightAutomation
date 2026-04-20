from playwright.sync_api import Page, Locator, expect
from config.settings import settings


class BasePage:
    """Base page object — all page objects inherit from this."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(settings.DEFAULT_TIMEOUT)
        self.page.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT)

    def navigate(self, path: str = "") -> None:
        url = f"{settings.BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    def wait_for_load(self) -> None:
        self.page.wait_for_load_state("networkidle")

    def take_screenshot(self, name: str) -> None:
        self.page.screenshot(path=f"reports/screenshots/{name}.png", full_page=True)

    def reload(self) -> None:
        self.page.reload()

    def go_back(self) -> None:
        self.page.go_back()

    def element(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def fill(self, selector: str, value: str) -> None:
        self.page.locator(selector).fill(value)

    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    def expect_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text(self, selector: str, text: str) -> None:
        expect(self.page.locator(selector)).to_have_text(text)

    def expect_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(f".*{fragment}.*")
