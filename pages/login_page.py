from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login / sign-in page."""

    # Locators - Found via Playwright MCP inspection
    USERNAME_INPUT = "#sso_id"  # input[name='sso_id']
    PASSWORD_INPUT = "#sso_password"  # input[name='sso_password']
    SUBMIT_BUTTON = "#btnLogin"  # button[name='btnLogin'][type='submit']
    ERROR_MESSAGE = "[data-testid='error-message'], .error, .alert-danger, #error"
    REMEMBER_ME = "input[type='checkbox'][name='remember']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "LoginPage":
        self.navigate("/login")
        return self

    def login(self, username: str, password: str) -> None:
        self.page.locator(self.USERNAME_INPUT).fill(username)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.SUBMIT_BUTTON).click()

    def get_error_message(self) -> str:
        return self.page.locator(self.ERROR_MESSAGE).inner_text()

    def expect_error_visible(self) -> None:
        expect(self.page.locator(self.ERROR_MESSAGE)).to_be_visible()

    def expect_login_form_visible(self) -> None:
        expect(self.page.locator(self.USERNAME_INPUT)).to_be_visible()
        expect(self.page.locator(self.PASSWORD_INPUT)).to_be_visible()
        expect(self.page.locator(self.SUBMIT_BUTTON)).to_be_visible()
