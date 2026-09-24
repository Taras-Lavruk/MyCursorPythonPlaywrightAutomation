"""
Base page object — all page objects inherit from this class.

Provides:
- URL navigation helpers
- Module-level logger (use self._logger in subclasses)
- Popup / overlay dismissal via utils.helpers.dismiss_popups
- Common expect() wrappers

Guidelines:
- Do NOT add generic fill/click/element wrappers here — they duplicate
  Playwright's API and add a leaky abstraction layer.
- Every public method must have a full return-type annotation.
- Never call page.wait_for_timeout() — use explicit locator waits instead.
"""

import logging
import os
import re

from playwright.sync_api import Locator, Page, expect

from config.settings import settings
from utils.helpers import dismiss_popups

_logger = logging.getLogger(__name__)


class BasePage:
    """Root page object — contains only behaviour shared by every page."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self._logger = logging.getLogger(self.__class__.__module__ + "." + self.__class__.__name__)
        self.page.set_default_timeout(settings.DEFAULT_TIMEOUT)
        self.page.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT)

    # ── Navigation ────────────────────────────────────────────────────────────

    def navigate(self, path: str = "") -> None:
        """Navigate to BASE_URL + path."""
        url = f"{settings.BASE_URL}/{path.lstrip('/')}"
        self._logger.debug("Navigating to: %s", url)
        self.page.goto(url)

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def wait_for_load(self) -> None:
        """Wait for the page to reach networkidle state."""
        self.page.wait_for_load_state("networkidle")

    def reload(self) -> None:
        """Reload the current page."""
        self.page.reload()

    def go_back(self) -> None:
        """Navigate to the previous page in browser history."""
        self.page.go_back()

    # ── Locator shortcuts ─────────────────────────────────────────────────────

    def locator(self, selector: str) -> Locator:
        """Return a Playwright Locator for the given CSS/XPath selector."""
        return self.page.locator(selector)

    # ── Assertions ────────────────────────────────────────────────────────────

    def expect_visible(self, selector: str) -> None:
        """Assert the element matching selector is visible (with auto-retry)."""
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text(self, selector: str, text: str) -> None:
        """Assert the element has the given text (with auto-retry)."""
        expect(self.page.locator(selector)).to_have_text(text)

    def expect_url_contains(self, fragment: str) -> None:
        """Assert the current URL contains fragment (substring match via regex)."""
        expect(self.page).to_have_url(re.compile(re.escape(fragment)))

    # ── Screenshots ───────────────────────────────────────────────────────────

    def take_screenshot(self, name: str) -> None:
        """Capture a full-page screenshot to reports/screenshots/<name>.png."""
        os.makedirs("reports/screenshots", exist_ok=True)
        path = f"reports/screenshots/{name}.png"
        self.page.screenshot(path=path, full_page=True)
        self._logger.debug("Screenshot saved: %s", path)

    # ── Popup / overlay dismissal ─────────────────────────────────────────────

    def dismiss_popups(self) -> None:
        """Dismiss cookie banners, license messages, and alert overlays."""
        dismiss_popups(self.page)

    def accept_cookies(self) -> None:
        """Accept the Atlassian cookie-consent banner if present.

        Uses is_visible() + wait_for(state='hidden') — no arbitrary sleep.
        """
        btn = self.page.locator("button:has-text('Accept all')").first
        if btn.is_visible(timeout=3000):
            btn.click()
            btn.wait_for(state="hidden", timeout=3000)
            self._logger.debug("Cookie banner accepted")

    def dismiss_license_message(self) -> None:
        """Close the license error banner if present."""
        close_link = self.page.locator("#licenseMessage a, .licenseErrorMessage a").first
        if close_link.is_visible(timeout=2000):
            close_link.click()
            page_banner = self.page.locator("#licenseMessage, .licenseErrorMessage").first
            page_banner.wait_for(state="hidden", timeout=3000)
            self._logger.debug("License message dismissed")

    def is_cookie_banner_visible(self) -> bool:
        """Return True if the cookie consent banner is currently visible."""
        return self.page.locator(
            "[role='dialog'][aria-labelledby='cookiesTrackingNoticeLink'], [id*='cookie']"
        ).is_visible(timeout=2000)
