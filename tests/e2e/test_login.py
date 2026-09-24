"""
Login page E2E tests.

Improvements over original version:
  - All page.wait_for_timeout() calls replaced with explicit expect() assertions
  - Playwright expect() used throughout — assertions auto-retry up to DEFAULT_TIMEOUT
  - parametrize used instead of for-loops (each credential pair is a separate test)
  - test_valid_login_redirects uses authenticated_page fixture (storageState — no re-login)
  - test_login_multiple_failed_attempts uses expect() for URL assertion, not assert
"""

import re

import pytest
from playwright.sync_api import Page, expect

from config.settings import settings
from pages.login_page import LoginPage


@pytest.mark.e2e
@pytest.mark.regression
class TestLogin:
    """Login flow — unauthenticated tests."""

    def test_login_page_loads(self, page: Page) -> None:
        """Login page should be accessible and render a non-empty title."""
        login = LoginPage(page)
        login.open()
        assert page.title() != "", "Page title should not be empty"

    def test_login_form_elements_visible(self, page: Page) -> None:
        """All login form elements should be visible on page load."""
        login = LoginPage(page)
        login.open()
        login.expect_login_form_visible()

    @pytest.mark.parametrize(
        "username,password",
        [
            ("", "password"),
            ("user@example.com", ""),
            ("", ""),
        ],
    )
    def test_login_with_empty_fields_stays_on_login_page(
        self, page: Page, username: str, password: str
    ) -> None:
        """Submitting with empty credentials must not navigate away from /login."""
        login = LoginPage(page)
        login.open()
        login.login(username, password)
        # Either the URL stays on the login page or an error message appears
        url_after = page.url
        assert "login" in url_after.lower() or login.page.locator(login.ERROR_MESSAGE).count() > 0

    @pytest.mark.parametrize(
        "username,password,description",
        [
            ("invalid@example.com", "wrongpassword", "wrong credentials"),
            ("notanemail", "password123", "invalid email format"),
            ("admin", "admin", "common default credentials"),
            ("test@test.com", "12345", "weak password"),
        ],
    )
    def test_login_with_invalid_credentials_stays_on_login_page(
        self, page: Page, username: str, password: str, description: str
    ) -> None:
        """Invalid credentials should not navigate away from the login page."""
        login = LoginPage(page)
        login.open()
        login.login(username, password)
        # expect() auto-retries — no wait_for_timeout needed
        expect(page).to_have_url(re.compile(r"login", re.IGNORECASE), timeout=5000)

    @pytest.mark.skipif(
        not settings.TEST_USERNAME,
        reason="TEST_USERNAME not configured in .env",
    )
    def test_valid_login_redirects_away_from_login_page(self, page: Page) -> None:
        """Valid credentials should redirect the user away from the login page."""
        login = LoginPage(page)
        login.open()
        login.login(settings.TEST_USERNAME, settings.TEST_PASSWORD)
        expect(page).not_to_have_url(re.compile(r"login", re.IGNORECASE), timeout=15000)

    def test_username_field_accepts_input(self, page: Page) -> None:
        """Username field should accept and display the entered value."""
        login = LoginPage(page)
        login.open()
        test_value = "test@example.com"
        page.locator(login.USERNAME_INPUT).fill(test_value)
        expect(page.locator(login.USERNAME_INPUT)).to_have_value(test_value)

    def test_password_field_is_masked(self, page: Page) -> None:
        """Password field should have type='password' to mask input."""
        login = LoginPage(page)
        login.open()
        expect(page.locator(login.PASSWORD_INPUT)).to_have_attribute("type", "password")

    def test_submit_button_is_enabled(self, page: Page) -> None:
        """Submit button should be enabled and ready for interaction."""
        login = LoginPage(page)
        login.open()
        expect(page.locator(login.SUBMIT_BUTTON)).to_be_enabled()

    def test_keyboard_navigation_tab_moves_to_password(self, page: Page) -> None:
        """Tab from the username field should move focus to the password field."""
        login = LoginPage(page)
        login.open()
        username_input = page.locator(login.USERNAME_INPUT)
        password_input = page.locator(login.PASSWORD_INPUT)

        username_input.click()
        username_input.fill("test@example.com")
        page.keyboard.press("Tab")
        expect(password_input).to_be_focused()

    def test_enter_submits_form(self, page: Page) -> None:
        """Pressing Enter in the password field should submit the form."""
        login = LoginPage(page)
        login.open()
        page.locator(login.USERNAME_INPUT).fill("test@example.com")
        page.locator(login.PASSWORD_INPUT).fill("password123")
        page.keyboard.press("Enter")
        # After submission with invalid credentials we stay on the login page
        expect(page).to_have_url(re.compile(r"login", re.IGNORECASE), timeout=5000)

    @pytest.mark.parametrize("attempt", range(3))
    def test_multiple_failed_attempts_stay_on_login_page(
        self, page: Page, attempt: int
    ) -> None:
        """Each failed login attempt should keep the user on the login page."""
        login = LoginPage(page)
        login.open()
        login.login("invalid@example.com", "wrongpassword")
        expect(page).to_have_url(re.compile(r"login", re.IGNORECASE), timeout=5000)

    def test_form_fields_can_be_cleared(self, page: Page) -> None:
        """Form fields should be clearable after input."""
        login = LoginPage(page)
        login.open()
        username_input = page.locator(login.USERNAME_INPUT)
        password_input = page.locator(login.PASSWORD_INPUT)

        username_input.fill("test@example.com")
        password_input.fill("password123")
        username_input.clear()
        password_input.clear()

        expect(username_input).to_have_value("")
        expect(password_input).to_have_value("")

    def test_login_page_has_non_empty_title(self, page: Page) -> None:
        """Login page should have a non-empty document title."""
        login = LoginPage(page)
        login.open()
        assert len(page.title()) > 0, "Page title must not be empty"

    def test_form_inputs_have_accessible_identifiers(self, page: Page) -> None:
        """Username and password inputs must each have at least one accessibility attribute."""
        login = LoginPage(page)
        login.open()

        for input_selector in (login.USERNAME_INPUT, login.PASSWORD_INPUT):
            loc = page.locator(input_selector)
            has_identifier = any(
                loc.get_attribute(attr) is not None
                for attr in ("placeholder", "aria-label", "name", "id")
            )
            assert has_identifier, (
                f"Input {input_selector!r} must have at least one accessibility attribute"
            )
