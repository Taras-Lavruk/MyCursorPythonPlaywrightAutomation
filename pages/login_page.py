"""
LoginPage — page object for the Jira Align sign-in page.

Locators were confirmed via Playwright MCP DOM inspection:
  #sso_id        → username input  (name='sso_id')
  #sso_password  → password input  (name='sso_password')
  #btnLogin      → submit button   (name='btnLogin', type='submit')
"""

import logging

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

_logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page object for the /login route."""

    # ── Locators ──────────────────────────────────────────────────────────────
    USERNAME_INPUT = "#sso_id"
    PASSWORD_INPUT = "#sso_password"
    SUBMIT_BUTTON = "#btnLogin"
    ERROR_MESSAGE = "[data-testid='error-message'], .error, .alert-danger, #error"
    REMEMBER_ME = "input[type='checkbox'][name='remember']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ───────────────────────────────────────────────────────────────

    def open(self) -> "LoginPage":
        """Navigate to the login page and return self for method chaining."""
        self.navigate("/login")
        self._logger.debug("Login page opened: %s", self.page.url)
        return self

    def login(self, username: str, password: str) -> None:
        """Fill credentials and submit the login form."""
        self._logger.info("Attempting login as: %s", username)
        self.page.locator(self.USERNAME_INPUT).fill(username)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.SUBMIT_BUTTON).click()

    def get_error_message(self) -> str:
        """Return the text of the visible error message, if any."""
        return self.page.locator(self.ERROR_MESSAGE).inner_text()

    # ── Assertions ────────────────────────────────────────────────────────────

    def expect_error_visible(self) -> None:
        """Assert the error message element is visible."""
        expect(self.page.locator(self.ERROR_MESSAGE)).to_be_visible()

    def expect_login_form_visible(self) -> None:
        """Assert all three form elements are visible and ready for input."""
        expect(self.page.locator(self.USERNAME_INPUT)).to_be_visible()
        expect(self.page.locator(self.PASSWORD_INPUT)).to_be_visible()
        expect(self.page.locator(self.SUBMIT_BUTTON)).to_be_visible()
