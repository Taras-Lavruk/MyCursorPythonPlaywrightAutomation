"""
HomePage — authenticated Jira Align landing page.

This page has NO left sidebar — only the shared top navigation header.
Users are redirected here after a successful login.
"""

import logging
import re

from playwright.sync_api import Page, expect

from pages.header_page import HeaderPage

_logger = logging.getLogger(__name__)


class HomePage(HeaderPage):
    """Page object for the post-login home/dashboard page."""

    # ── Locators ──────────────────────────────────────────────────────────────
    ALERT_BANNER = "[role='alert']"
    ALERT_CLOSE_BUTTON = "[role='alert'] button"

    RECENT_ROOMS_HEADING = "h3:has-text('Recent rooms')"
    STARRED_HEADING = "h3:has-text('Starred')"
    STARRED_VIEW_ALL = "a:has-text('View all')"

    PORTFOLIO_CARDS = ".card, [class*='portfolio'], [class*='card']"
    CARD_TITLES = "[class*='card'] h4, [class*='card'] h3"

    MAIN_CONTENT = "main, [role='main']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Alert banner ──────────────────────────────────────────────────────────

    def dismiss_alert_banner(self) -> None:
        """Dismiss the alert banner if it is present."""
        close_btn = self.page.locator(self.ALERT_CLOSE_BUTTON).first
        if close_btn.is_visible(timeout=2000):
            close_btn.click()
            self.page.locator(self.ALERT_BANNER).first.wait_for(state="hidden", timeout=3000)
            self._logger.debug("Alert banner dismissed")

    def get_alert_message(self) -> str:
        """Return the text content of the first alert banner."""
        return self.page.locator(self.ALERT_BANNER).first.inner_text()

    # ── Content section helpers ───────────────────────────────────────────────

    def is_recent_rooms_visible(self) -> bool:
        """Return True if the 'Recent rooms' section heading is visible."""
        return self.page.locator(self.RECENT_ROOMS_HEADING).is_visible()

    def is_starred_section_visible(self) -> bool:
        """Return True if the 'Starred' section heading is visible."""
        return self.page.locator(self.STARRED_HEADING).is_visible()

    def get_portfolio_cards_count(self) -> int:
        """Return the number of portfolio/program cards displayed."""
        return self.page.locator(self.PORTFOLIO_CARDS).count()

    def get_card_titles(self) -> list[str]:
        """Return the titles of all visible portfolio/program cards."""
        return self.page.locator(self.CARD_TITLES).all_inner_texts()

    def click_portfolio_card(self, title: str) -> None:
        """Click a portfolio/program card identified by its title."""
        self.page.locator(f"{self.CARD_TITLES}:has-text('{title}')").first.click()

    def click_view_all_starred(self) -> None:
        """Click the 'View all' link in the Starred section."""
        self.page.locator(self.STARRED_VIEW_ALL).click()

    # ── Assertions ────────────────────────────────────────────────────────────

    def expect_loaded(self) -> None:
        """Assert the home page is fully loaded after login."""
        # Jira Align appends section names to the title (e.g. "Jira Align | Home"),
        # so use a substring match rather than an exact string.
        expect(self.page).to_have_title(re.compile(r"Jira Align", re.IGNORECASE))
        self.wait_for_load()
        self.expect_header_visible()

    def expect_main_content_visible(self) -> None:
        """Assert the main content area is visible."""
        expect(self.page.locator(self.MAIN_CONTENT).first).to_be_visible()

    def expect_home_sections_visible(self) -> None:
        """Assert both the 'Recent rooms' and 'Starred' sections are visible."""
        expect(self.page.locator(self.RECENT_ROOMS_HEADING)).to_be_visible()
        expect(self.page.locator(self.STARRED_HEADING)).to_be_visible()
