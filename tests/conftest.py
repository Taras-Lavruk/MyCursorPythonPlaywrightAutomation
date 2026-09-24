"""
tests/conftest.py — test-layer fixtures shared across all test sub-packages.

The authenticated_page / authenticated_context fixtures are defined in the
ROOT conftest.py (using storageState) and are available here automatically.
This file provides only test-data and page-object convenience fixtures that
should not live at the root level.

Fixtures provided here:
  login_page          — LoginPage instance for unauthenticated tests
  test_credentials    — dict with username/password from settings
"""

import pytest
from playwright.sync_api import Page

from config.settings import settings
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Return a LoginPage instance backed by the unauthenticated ``page`` fixture."""
    return LoginPage(page)


@pytest.fixture
def test_credentials() -> dict[str, str]:
    """Return valid test credentials from settings (skip if not configured)."""
    if not settings.has_credentials:
        pytest.skip("TEST_USERNAME / TEST_PASSWORD not configured in .env")
    return {
        "username": settings.TEST_USERNAME,
        "password": settings.TEST_PASSWORD,
    }
