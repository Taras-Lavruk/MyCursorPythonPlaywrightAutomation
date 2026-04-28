from playwright.sync_api import Page, Locator, expect
from config.settings import settings


class BasePage:
    """Base page object — all page objects inherit from this."""
    
    # Cookie consent banner - Atlassian cookies dialog
    COOKIE_BANNER = "[role='dialog'][aria-labelledby='cookiesTrackingNoticeLink'], [id*='cookie'], [class*='cookie-banner']"
    COOKIE_ACCEPT_BUTTON = "button:has-text('Accept all'), [role='dialog'] button:has-text('Accept')"

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
    
    def accept_cookies(self, timeout: int = 5000) -> None:
        """Accept cookies if the banner is present."""
        try:
            cookie_button = self.page.locator(self.COOKIE_ACCEPT_BUTTON).first
            if cookie_button.is_visible(timeout=timeout):
                cookie_button.click()
                self.page.wait_for_timeout(500)
        except Exception:
            pass
    
    def is_cookie_banner_visible(self) -> bool:
        """Check if cookie consent banner is visible."""
        return self.page.locator(self.COOKIE_BANNER).is_visible(timeout=2000)
    
    def dismiss_license_message(self) -> None:
        """Dismiss the license error message if present."""
        try:
            license_close = self.page.locator("#licenseMessage a, .licenseErrorMessage a").first
            if license_close.is_visible(timeout=2000):
                license_close.click()
                self.page.wait_for_timeout(500)
        except Exception:
            pass
