"""
Shared test data / fixture factories for user-related tests.
"""
import pytest
from dataclasses import dataclass
from utils.helpers import random_email, random_string


@dataclass
class UserCredentials:
    username: str
    password: str


@pytest.fixture
def guest_user() -> UserCredentials:
    """Returns credentials for a one-off guest / throwaway user."""
    return UserCredentials(
        username=random_email(),
        password=random_string(12),
    )


@pytest.fixture
def admin_user() -> UserCredentials:
    """Returns admin credentials from env (skip if not configured)."""
    from config.settings import settings
    if not settings.TEST_USERNAME:
        pytest.skip("Admin credentials not configured")
    return UserCredentials(
        username=settings.TEST_USERNAME,
        password=settings.TEST_PASSWORD,
    )
