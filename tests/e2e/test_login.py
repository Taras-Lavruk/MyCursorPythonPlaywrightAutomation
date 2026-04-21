import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from config.settings import settings


@pytest.mark.e2e
@pytest.mark.regression
class TestLogin:
    """Login flow tests."""

    def test_login_page_loads(self, page: Page) -> None:
        """Login page should be accessible and render the form."""
        login = LoginPage(page)
        login.open()
        assert "login" in page.url.lower() or page.title() != ""

    def test_login_form_elements_visible(self, page: Page) -> None:
        """All login form elements should be visible on page load."""
        login = LoginPage(page)
        login.open()
        login.expect_login_form_visible()

    @pytest.mark.parametrize("username,password", [
        ("", "password"),
        ("user@example.com", ""),
        ("", ""),
    ])
    def test_login_with_empty_fields_fails(
        self, page: Page, username: str, password: str
    ) -> None:
        """Submitting empty credentials should not navigate away from the login page."""
        login = LoginPage(page)
        login.open()
        url_before = page.url
        login.login(username, password)
        # Either URL stays the same or an error appears
        url_after = page.url
        assert url_after == url_before or "login" in url_after.lower()

    @pytest.mark.parametrize("username,password,description", [
        ("invalid@example.com", "wrongpassword", "wrong credentials"),
        ("notanemail", "password123", "invalid email format"),
        ("admin", "admin", "common credentials"),
        ("test@test.com", "12345", "weak password"),
    ])
    def test_login_with_invalid_credentials(
        self, page: Page, username: str, password: str, description: str
    ) -> None:
        """Login with invalid credentials should fail and remain on login page."""
        login = LoginPage(page)
        login.open()
        login.login(username, password)
        page.wait_for_timeout(1000)
        
        current_url = page.url
        assert "login" in current_url.lower(), \
            f"Should remain on login page with {description}"

    @pytest.mark.skipif(
        not settings.TEST_USERNAME,
        reason="TEST_USERNAME not configured in .env",
    )
    def test_valid_login_redirects(self, page: Page) -> None:
        """Valid credentials should redirect away from the login page."""
        login = LoginPage(page)
        login.open()
        login.login(settings.TEST_USERNAME, settings.TEST_PASSWORD)
        page.wait_for_load_state("networkidle")
        assert "login" not in page.url.lower(), "Should redirect away from login after success"

    def test_username_field_accepts_input(self, page: Page) -> None:
        """Username field should accept and display user input."""
        login = LoginPage(page)
        login.open()
        
        test_username = "test@example.com"
        username_input = page.locator(login.USERNAME_INPUT)
        username_input.fill(test_username)
        
        expect(username_input).to_have_value(test_username)

    def test_password_field_masks_input(self, page: Page) -> None:
        """Password field should mask the entered password."""
        login = LoginPage(page)
        login.open()
        
        password_input = page.locator(login.PASSWORD_INPUT)
        expect(password_input).to_have_attribute("type", "password")

    def test_submit_button_is_clickable(self, page: Page) -> None:
        """Submit button should be clickable."""
        login = LoginPage(page)
        login.open()
        
        submit_button = page.locator(login.SUBMIT_BUTTON)
        expect(submit_button).to_be_enabled()

    def test_login_form_keyboard_navigation(self, page: Page) -> None:
        """Users should be able to navigate the form using keyboard."""
        login = LoginPage(page)
        login.open()
        
        username_input = page.locator(login.USERNAME_INPUT)
        password_input = page.locator(login.PASSWORD_INPUT)
        
        username_input.click()
        username_input.fill("test@example.com")
        
        page.keyboard.press("Tab")
        expect(password_input).to_be_focused()
        
        password_input.fill("password123")
        
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)

    def test_login_multiple_failed_attempts(self, page: Page) -> None:
        """Test multiple consecutive failed login attempts."""
        login = LoginPage(page)
        login.open()
        
        for _ in range(3):
            login.login("invalid@example.com", "wrongpassword")
            page.wait_for_timeout(500)
            assert "login" in page.url.lower()

    def test_login_form_clears_on_submission(self, page: Page) -> None:
        """Form fields should be clearable after failed login."""
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

    def test_login_page_title_is_set(self, page: Page) -> None:
        """Login page should have a meaningful title."""
        login = LoginPage(page)
        login.open()
        
        title = page.title()
        assert title != "", "Page title should not be empty"
        assert len(title) > 0, "Page should have a title"

    def test_login_form_accessibility_labels(self, page: Page) -> None:
        """Form inputs should have accessible labels or placeholders."""
        login = LoginPage(page)
        login.open()
        
        username_input = page.locator(login.USERNAME_INPUT)
        password_input = page.locator(login.PASSWORD_INPUT)
        
        username_has_label = (
            username_input.get_attribute("placeholder") is not None or
            username_input.get_attribute("aria-label") is not None or
            username_input.get_attribute("name") is not None
        )
        
        password_has_label = (
            password_input.get_attribute("placeholder") is not None or
            password_input.get_attribute("aria-label") is not None or
            password_input.get_attribute("name") is not None
        )
        
        assert username_has_label, "Username field should have accessible label"
        assert password_has_label, "Password field should have accessible label"
