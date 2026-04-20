import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from config.settings import settings


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Fixture that provides a LoginPage instance."""
    return LoginPage(page)


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """
    Fixture that provides a page with an already logged-in user.
    Useful for tests that need to start from an authenticated state.
    """
    if not settings.TEST_USERNAME or not settings.TEST_PASSWORD:
        pytest.skip("Valid credentials not configured in .env")
    
    login = LoginPage(page)
    login.open()
    login.login(settings.TEST_USERNAME, settings.TEST_PASSWORD)
    page.wait_for_load_state("networkidle")
    
    if "login" in page.url.lower():
        pytest.fail("Failed to login with provided credentials")
    
    return page


@pytest.fixture
def test_credentials():
    """Fixture that provides test credentials from settings."""
    return {
        "username": settings.TEST_USERNAME,
        "password": settings.TEST_PASSWORD,
    }


@pytest.fixture
def invalid_credentials():
    """Fixture that provides various invalid credential sets."""
    return [
        {"username": "invalid@example.com", "password": "wrongpassword"},
        {"username": "notanemail", "password": "password123"},
        {"username": "", "password": "password"},
        {"username": "user@test.com", "password": ""},
    ]
