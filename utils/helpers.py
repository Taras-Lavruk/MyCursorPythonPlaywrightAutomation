"""
General-purpose utility functions.

Most helpers in this module are pure Python with no external dependencies and
can be imported freely by any layer (pages, fixtures, tests, config).

The ``dismiss_popups`` function is the one exception: it imports
``playwright.sync_api.Page`` because it is a shared UI utility used by
conftest.py, page objects, and tests alike. ``pytest`` is intentionally NOT
imported here so this module stays usable outside a test session.
"""

import logging
import random
import re
import string

from faker import Faker
from playwright.sync_api import Page

_logger = logging.getLogger(__name__)
fake = Faker()


# ---------------------------------------------------------------------------
# Random data generators
# ---------------------------------------------------------------------------

def random_string(length: int = 8) -> str:
    """Return a random lowercase ASCII string of the given length."""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    """Return a random fake email address."""
    return fake.email()


def random_phone() -> str:
    """Return a random fake phone number."""
    return fake.phone_number()


def random_name() -> str:
    """Return a random fake full name."""
    return fake.name()


# ---------------------------------------------------------------------------
# String utilities
# ---------------------------------------------------------------------------

def normalize_whitespace(text: str) -> str:
    """Collapse multiple whitespace characters into a single space."""
    return re.sub(r"\s+", " ", text).strip()


def extract_numbers(text: str) -> list[int]:
    """Extract all integer sequences from a string."""
    return [int(n) for n in re.findall(r"\d+", text)]


def format_url(base: str, path: str) -> str:
    """Safely join a base URL and a path, avoiding double slashes."""
    return f"{base.rstrip('/')}/{path.lstrip('/')}"


# ---------------------------------------------------------------------------
# UI popup / overlay dismissal
# ---------------------------------------------------------------------------

def dismiss_popups(page: Page) -> None:
    """Dismiss any overlays that block test interactions on Jira Align pages.

    Handles three known overlays:
    1. Atlassian cookie-consent banner ("Accept all" button)
    2. License-error message bar (#licenseMessage / .licenseErrorMessage)
    3. Generic [role='alert'] banner with a close button

    Uses ``is_visible()`` to check presence and ``wait_for(state='hidden')``
    after clicking — no arbitrary sleeps.
    """
    # 1 — Cookie consent banner
    accept_btn = page.locator("button:has-text('Accept all')").first
    if accept_btn.is_visible(timeout=2000):
        accept_btn.click()
        accept_btn.wait_for(state="hidden", timeout=3000)
        _logger.debug("Cookie banner dismissed")

    # 2a — License error message (link-based close)
    license_close = page.locator("#licenseMessage a, .licenseErrorMessage a").first
    if license_close.is_visible(timeout=1000):
        license_close.click()
        page.locator("#licenseMessage, .licenseErrorMessage").first.wait_for(
            state="hidden", timeout=3000
        )
        _logger.debug("License message dismissed")

    # 3 — Generic alert banner with a button
    alert_btn = page.locator("[role='alert'] button").first
    if alert_btn.is_visible(timeout=500):
        alert_btn.click()
        page.locator("[role='alert']").first.wait_for(state="hidden", timeout=3000)
        _logger.debug("Alert banner dismissed")
