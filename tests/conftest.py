import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.home_page import HomePage
from config.settings import settings


def dismiss_popups(page: Page, max_attempts: int = 3) -> None:
    """Helper function to aggressively dismiss cookies and alerts that appear during tests.
    
    This function handles:
    - Atlassian cookie dialog ("Accept all" button)
    - License error message (custom to this app)
    - Standard alert banners
    
    Args:
        page: Playwright Page object
        max_attempts: Maximum number of times to try dismissing popups (default 3)
    """
    for attempt in range(max_attempts):
        popup_dismissed = False
        
        # Dismiss cookie dialog
        try:
            accept_all_btn = page.locator("button:has-text('Accept all')").first
            if accept_all_btn.is_visible(timeout=800):
                accept_all_btn.click()
                page.wait_for_timeout(500)
                popup_dismissed = True
        except Exception:
            pass
        
        # Dismiss license error message (custom banner)
        try:
            license_close = page.locator("#licenseMessage a, .licenseErrorMessage a").first
            if license_close.is_visible(timeout=500):
                license_close.click()
                page.wait_for_timeout(300)
                popup_dismissed = True
        except Exception:
            pass
        
        # Dismiss standard alert banner
        try:
            alert_btn = page.locator("[role='alert'] button, .alert button").first
            if alert_btn.is_visible(timeout=500):
                alert_btn.click()
                page.wait_for_timeout(300)
                popup_dismissed = True
        except Exception:
            pass
        
        # If no popup was dismissed, we're done
        if not popup_dismissed:
            break


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Fixture that provides a LoginPage instance."""
    return LoginPage(page)


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """
    Fixture that provides a page with an already logged-in user.
    Automatically handles:
    - Cookie acceptance before login
    - Cookie acceptance after login (banner reappears!)
    - Alert banner dismissal after login
    
    Useful for tests that need to start from an authenticated state.
    """
    if not settings.TEST_USERNAME or not settings.TEST_PASSWORD:
        pytest.skip("Valid credentials not configured in .env")
    
    login = LoginPage(page)
    login.open()
    
    # Dismiss cookies before login
    dismiss_popups(page, max_attempts=2)
    
    # Login
    login.login(settings.TEST_USERNAME, settings.TEST_PASSWORD)
    page.wait_for_load_state("networkidle")
    
    if "login" in page.url.lower():
        pytest.fail("Failed to login with provided credentials")
    
    # Cookie dialog and license message reappear after login! Wait and dismiss
    page.wait_for_timeout(2000)
    dismiss_popups(page, max_attempts=3)
    
    return page


@pytest.fixture
def authenticated_page(page: Page) -> Page:
    """
    Alias for logged_in_page fixture.
    Provides a fully authenticated page with cookies accepted and alerts dismissed.
    
    Use this fixture for any test that requires authentication.
    Example:
        def test_something(authenticated_page: Page):
            home = HomePage(authenticated_page)
            # Your test code here
    """
    if not settings.TEST_USERNAME or not settings.TEST_PASSWORD:
        pytest.skip("Valid credentials not configured in .env")
    
    login = LoginPage(page)
    login.open()
    
    # Dismiss cookies before login
    dismiss_popups(page, max_attempts=2)
    
    # Login
    login.login(settings.TEST_USERNAME, settings.TEST_PASSWORD)
    page.wait_for_load_state("networkidle")
    
    if "login" in page.url.lower():
        pytest.fail("Failed to login with provided credentials")
    
    # Cookie dialog and license message reappear after login! Wait and dismiss
    page.wait_for_timeout(3000)  # Wait longer for popups to appear
    dismiss_popups(page, max_attempts=5)
    print("✓ All popups dismissed after login")
    
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
