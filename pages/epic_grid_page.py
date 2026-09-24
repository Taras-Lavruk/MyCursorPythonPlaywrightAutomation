"""
EpicGridPage — Jira Align Epics data grid.

URL pattern: /EpicGrid?Portfolios={id}&Releases={id}&FilterID={id}

Inherits:
  BasePage → HeaderPage → SidebarPage → GridPage → EpicGridPage
"""

import logging
import re

from playwright.sync_api import Page, expect

from pages.grid_page import GridPage

_logger = logging.getLogger(__name__)


class EpicGridPage(GridPage):
    """Page object for the Epics grid page."""

    # ── Sidebar navigation links (scoped to aside to avoid header collisions) ──
    # Portfolio room links are dynamic — match by href pattern, not by room display name.
    SIDEBAR_PORTFOLIO_ROOM = "aside a[href*='PortfolioRoom' i], aside a[href*='portfolio-room' i]"
    SIDEBAR_EPICS = "aside a:has-text('Epics')"
    SIDEBAR_BACKLOG = "aside a:has-text('Backlog')"
    SIDEBAR_ROADMAPS = "aside a:has-text('Roadmaps')"
    SIDEBAR_OKR_HUB = "aside a:has-text('OKR hub')"
    SIDEBAR_WORK_TREE = "aside a:has-text('Work tree')"
    SIDEBAR_FORECAST = "aside a:has-text('Forecast')"
    SIDEBAR_CAPACITY = "aside a:has-text('Capacity')"

    # ── Epic grid columns ──────────────────────────────────────────────────────
    COLUMN_ID = "th:has-text('ID')"
    COLUMN_EXT_ID = "th:has-text('Ext ID')"
    COLUMN_TITLE = "th:has-text('Title')"
    COLUMN_STATE = "th:has-text('State')"
    COLUMN_OWNER = "th:has-text('Owner')"
    COLUMN_TAGS = "th:has-text('Tags')"

    # ── Epic-specific action buttons ───────────────────────────────────────────
    IMPORT_EPICS_BUTTON = "button:has-text('Import'), a:has-text('Import Epics')"
    EXPORT_EPICS_BUTTON = "button:has-text('Export'), a:has-text('Export Epics')"
    BOTTOM_UP_ESTIMATE_BUTTON = "button:has-text('Bottom-Up Estimate')"
    PRINT_EPIC_CARDS_BUTTON = "button:has-text('Print Epic Cards')"
    QUICK_ADD_EPIC = "button:has-text('Quick Add'), button:has-text('Add Epic')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Sidebar navigation ─────────────────────────────────────────────────────

    def navigate_to_portfolio_room(self) -> None:
        """Navigate to Portfolio Room from sidebar."""
        self.page.locator(self.SIDEBAR_PORTFOLIO_ROOM).click()

    def navigate_to_backlog(self) -> None:
        """Navigate to Backlog from sidebar."""
        self.page.locator(self.SIDEBAR_BACKLOG).click()

    def navigate_to_roadmaps(self) -> None:
        """Navigate to Roadmaps from sidebar."""
        self.page.locator(self.SIDEBAR_ROADMAPS).click()

    def navigate_to_work_tree(self) -> None:
        """Navigate to Work Tree from sidebar."""
        self.page.locator(self.SIDEBAR_WORK_TREE).click()

    # ── Epic-specific actions ──────────────────────────────────────────────────

    def quick_add_epic(self) -> None:
        """Open quick-add epic dialog."""
        btn = self.page.locator(self.QUICK_ADD_EPIC).first
        if btn.is_visible(timeout=0):
            btn.click()
            self._logger.debug("Quick-add epic opened")

    def import_epics(self) -> None:
        """Open import epics dialog."""
        btn = self.page.locator(self.IMPORT_EPICS_BUTTON).first
        if btn.is_visible(timeout=0):
            btn.click()

    def export_epics(self) -> None:
        """Export epics to file."""
        btn = self.page.locator(self.EXPORT_EPICS_BUTTON).first
        if btn.is_visible(timeout=0):
            btn.click()

    def open_bottom_up_estimate(self) -> None:
        """Open bottom-up estimation dialog."""
        btn = self.page.locator(self.BOTTOM_UP_ESTIMATE_BUTTON).first
        if btn.is_visible(timeout=0):
            btn.click()

    def print_epic_cards(self) -> None:
        """Print epic cards."""
        btn = self.page.locator(self.PRINT_EPIC_CARDS_BUTTON).first
        if btn.is_visible(timeout=0):
            btn.click()

    # ── Data accessors ─────────────────────────────────────────────────────────

    def get_epic_ids(self) -> list[str]:
        """Return all epic IDs from the first table column."""
        return self.page.locator("table tbody td:first-child").all_inner_texts()

    def search_epic_by_title(self, title: str) -> None:
        """Search for an epic by title using the grid search box."""
        self.search_grid(title)

    def get_epic_count(self) -> int:
        """Return the number of epics currently visible in the grid."""
        return self.get_row_count()

    # ── Assertions ─────────────────────────────────────────────────────────────

    def expect_epic_grid_loaded(self) -> None:
        """Assert the epic grid URL, grid, header, and sidebar are all present."""
        expect(self.page).to_have_url(re.compile(r"/EpicGrid", re.IGNORECASE))
        self.expect_grid_visible()
        self.expect_header_visible()
        self.expect_sidebar_visible()

    def expect_epic_columns_visible(self) -> None:
        """Assert the core epic columns (ID, Title, State) are visible."""
        expect(self.page.locator(self.COLUMN_ID)).to_be_visible()
        expect(self.page.locator(self.COLUMN_TITLE)).to_be_visible()
        expect(self.page.locator(self.COLUMN_STATE)).to_be_visible()
