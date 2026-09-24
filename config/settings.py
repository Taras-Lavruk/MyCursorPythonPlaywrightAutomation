"""
Application settings — loaded from environment variables / .env file.

Uses pydantic-settings for type coercion, validation, and env-file support.
All values can be overridden via environment variables (case-insensitive).

Example:
    from config.settings import settings
    print(settings.BASE_URL)
    print(settings.BROWSER)          # BrowserType.CHROMIUM
    print(settings.BROWSER.value)    # "chromium"
"""

import os
from enum import Enum

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BrowserType(Enum):
    """Supported Playwright browser engines."""

    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


class Settings(BaseSettings):
    """Project-wide settings, resolved from .env → environment variables → defaults."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application URLs ────────────────────────────────────────────────────
    BASE_URL: str = "https://rc-manual.jiraalign.xyz"
    API_BASE_URL: str = "https://rc-manual.jiraalign.xyz/rest/align/api/2"
    API_BEARER_TOKEN: str = ""

    # ── Test credentials ────────────────────────────────────────────────────
    TEST_USERNAME: str = ""
    TEST_PASSWORD: str = ""

    # ── Browser settings ────────────────────────────────────────────────────
    HEADLESS: bool = True
    SLOW_MO: int = 0
    BROWSER: BrowserType = BrowserType.CHROMIUM
    RECORD_VIDEO: bool = False

    # ── Timeouts (ms) ───────────────────────────────────────────────────────
    DEFAULT_TIMEOUT: int = 30000
    NAVIGATION_TIMEOUT: int = 60000

    # ── Viewport ────────────────────────────────────────────────────────────
    VIEWPORT_WIDTH: int = 1280
    VIEWPORT_HEIGHT: int = 720

    # ── Validators ──────────────────────────────────────────────────────────
    @field_validator("BASE_URL", "API_BASE_URL", mode="before")
    @classmethod
    def strip_trailing_slash(cls, value: str) -> str:
        """Ensure URLs never have a trailing slash — prevents double-slash bugs."""
        return value.rstrip("/")

    # ── Convenience properties ───────────────────────────────────────────────
    @property
    def has_credentials(self) -> bool:
        """True when both TEST_USERNAME and TEST_PASSWORD are set."""
        return bool(self.TEST_USERNAME and self.TEST_PASSWORD)

    @property
    def auth_state_path(self) -> str:
        """File path used to persist browser storage state between test runs."""
        return os.path.join("auth", "state.json")


# Module-level singleton — import this everywhere.
settings = Settings()
