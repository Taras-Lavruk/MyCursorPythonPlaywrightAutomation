"""
SidebarPage — base class for pages that include a left navigation sidebar.

Portfolio rooms, grid pages (Epics, Stories, etc.) and Administration all
inherit from this class to get sidebar interaction methods.
"""

import logging

from playwright.sync_api import Page, expect

from pages.header_page import HeaderPage

_logger = logging.getLogger(__name__)


class SidebarPage(HeaderPage):
    """Adds left-sidebar navigation on top of the shared header."""

    # ── Locators ──────────────────────────────────────────────────────────────
    # Jira Align uses several container patterns across different pages.
    SIDEBAR_CONTAINER = (
        "aside, "
        "nav:not(header nav), "
        "[class*='sidebar'], "
        "[class*='side-nav'], "
        "[class*='admin-nav'], "
        "[id*='sidebar']"
    )
    SIDEBAR_TOGGLE_BUTTON = "button[aria-label*='sidebar' i], button[aria-label*='menu' i]"
    SIDEBAR_LINKS = f"{SIDEBAR_CONTAINER} a"
    SIDEBAR_ACTIVE_LINK = (
        "[class*='sidebar'] a[class*='active'], "
        "aside a[class*='active'], "
        "nav a[class*='active']"
    )

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Sidebar state ─────────────────────────────────────────────────────────

    def is_sidebar_visible(self) -> bool:
        """Return True if a sidebar container is present and visible."""
        return self.page.locator(self.SIDEBAR_CONTAINER).first.is_visible(timeout=0)

    def toggle_sidebar(self) -> None:
        """Toggle the sidebar if a toggle button is present."""
        toggle = self.page.locator(self.SIDEBAR_TOGGLE_BUTTON).first
        if toggle.is_visible(timeout=0):
            toggle.click()
            self._logger.debug("Sidebar toggled")

    # ── Link accessors ────────────────────────────────────────────────────────

    def get_sidebar_links(self) -> list[str]:
        """Return the text of all links in the sidebar."""
        if not self.is_sidebar_visible():
            self._logger.debug("Sidebar not visible — returning empty link list")
            return []
        return self.page.locator(self.SIDEBAR_LINKS).all_inner_texts()

    def get_active_sidebar_link(self) -> str:
        """Return the text of the currently active (highlighted) sidebar link."""
        active = self.page.locator(self.SIDEBAR_ACTIVE_LINK).first
        if active.is_visible(timeout=0):
            return active.inner_text()
        return ""

    # ── Assertions ────────────────────────────────────────────────────────────

    def expect_sidebar_visible(self) -> None:
        """Assert the sidebar container is visible."""
        expect(self.page.locator(self.SIDEBAR_CONTAINER).first).to_be_visible()
