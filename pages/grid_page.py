"""
GridPage — base class for all data-grid pages (Epics, Stories, Features, etc.).

All grid pages share: search, filters, pagination, column selector, and
action toolbars. Specific grid pages (EpicGridPage, StoryGridPage, etc.)
inherit from this class and add item-specific locators and actions.
"""

import logging

from playwright.sync_api import Page, expect

from pages.sidebar_page import SidebarPage

_logger = logging.getLogger(__name__)


class GridPage(SidebarPage):
    """Base page object for Jira Align data-grid views."""

    # ── Search & Filters ──────────────────────────────────────────────────────
    SEARCH_BOX = "input[type='search'], input[placeholder*='search' i]"
    FILTER_BUTTON = "button:has-text('Filter'), button[title*='filter' i]"
    CONFIGURATION_BAR = "[class*='config'], [class*='toolbar']"

    # ── Action toolbar ────────────────────────────────────────────────────────
    MORE_ACTIONS_DROPDOWN = "button:has-text('More Actions'), button:has-text('Actions')"
    STAR_PAGE_BUTTON = "button:has-text('Star Page')"
    SHARE_BUTTON = "button:has-text('Share')"
    EXPORT_BUTTON = "button:has-text('Export')"

    # ── Data grid ─────────────────────────────────────────────────────────────
    DATA_GRID = "table, [role='grid'], [class*='grid']"
    GRID_ROWS = "table tbody tr, [role='row']"
    GRID_HEADERS = "table thead th, [role='columnheader']"
    COLUMN_SELECTOR = "button:has-text('Columns'), button:has-text('Select Columns')"

    # ── Pagination ────────────────────────────────────────────────────────────
    PAGINATION_CONTAINER = "[class*='pagination'], .pagination"
    FIRST_PAGE_BUTTON = "button[title*='First' i]"
    PREVIOUS_PAGE_BUTTON = "button[title*='Previous' i]"
    NEXT_PAGE_BUTTON = "button[title*='Next' i]"
    LAST_PAGE_BUTTON = "button[title*='Last' i]"
    PAGE_INFO = "[class*='page-info'], .page-info"

    # ── Common actions ────────────────────────────────────────────────────────
    ADD_BUTTON = "button:has-text('Add'), button[title*='Add' i]"
    REFRESH_BUTTON = "button:has-text('Refresh'), button[title*='Refresh' i]"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Search & filter actions ───────────────────────────────────────────────

    def search_grid(self, query: str) -> None:
        """Type a search query into the search box and submit."""
        search = self.page.locator(self.SEARCH_BOX).first
        if search.is_visible(timeout=2000):
            search.fill(query)
            self.page.keyboard.press("Enter")
            self._logger.debug("Grid search submitted: %r", query)

    def clear_search(self) -> None:
        """Clear the search box."""
        search = self.page.locator(self.SEARCH_BOX).first
        if search.is_visible(timeout=2000):
            search.fill("")

    def open_filters(self) -> None:
        """Open the filter panel."""
        filter_btn = self.page.locator(self.FILTER_BUTTON).first
        if filter_btn.is_visible(timeout=2000):
            filter_btn.click()

    # ── Toolbar actions ───────────────────────────────────────────────────────

    def open_more_actions(self) -> None:
        """Open the 'More Actions' dropdown."""
        self.page.locator(self.MORE_ACTIONS_DROPDOWN).click()

    def star_page(self) -> None:
        """Star / favourite the current grid page."""
        btn = self.page.locator(self.STAR_PAGE_BUTTON).first
        if btn.is_visible(timeout=2000):
            btn.click()

    def click_share(self) -> None:
        """Click the Share button."""
        btn = self.page.locator(self.SHARE_BUTTON).first
        if btn.is_visible(timeout=2000):
            btn.click()

    def click_export(self) -> None:
        """Export grid data."""
        btn = self.page.locator(self.EXPORT_BUTTON).first
        if btn.is_visible(timeout=2000):
            btn.click()

    # ── Grid data accessors ───────────────────────────────────────────────────

    def get_row_count(self) -> int:
        """Return the number of visible data rows in the grid."""
        return self.page.locator(self.GRID_ROWS).count()

    def get_column_headers(self) -> list[str]:
        """Return the text of all column headers."""
        return self.page.locator(self.GRID_HEADERS).all_inner_texts()

    def open_column_selector(self) -> None:
        """Open the column visibility selector."""
        btn = self.page.locator(self.COLUMN_SELECTOR).first
        if btn.is_visible(timeout=2000):
            btn.click()

    # ── Pagination ────────────────────────────────────────────────────────────

    def go_to_first_page(self) -> None:
        """Navigate to the first page of results."""
        btn = self.page.locator(self.FIRST_PAGE_BUTTON).first
        if btn.is_visible(timeout=2000):
            btn.click()

    def go_to_previous_page(self) -> None:
        """Navigate to the previous page of results."""
        btn = self.page.locator(self.PREVIOUS_PAGE_BUTTON).first
        if btn.is_visible(timeout=2000):
            btn.click()

    def go_to_next_page(self) -> None:
        """Navigate to the next page of results."""
        btn = self.page.locator(self.NEXT_PAGE_BUTTON).first
        if btn.is_visible(timeout=2000):
            btn.click()

    def go_to_last_page(self) -> None:
        """Navigate to the last page of results."""
        btn = self.page.locator(self.LAST_PAGE_BUTTON).first
        if btn.is_visible(timeout=2000):
            btn.click()

    def get_page_info(self) -> str:
        """Return pagination summary text (e.g. 'Showing 1-20 of 100')."""
        info = self.page.locator(self.PAGE_INFO).first
        if info.is_visible(timeout=2000):
            return info.inner_text()
        return ""

    # ── Item creation ─────────────────────────────────────────────────────────

    def click_add(self) -> None:
        """Click the Add button to create a new item."""
        btn = self.page.locator(self.ADD_BUTTON).first
        if btn.is_visible(timeout=2000):
            btn.click()

    def refresh_grid(self) -> None:
        """Refresh the grid data."""
        btn = self.page.locator(self.REFRESH_BUTTON).first
        if btn.is_visible(timeout=2000):
            btn.click()

    # ── Assertions ────────────────────────────────────────────────────────────

    def expect_grid_visible(self) -> None:
        """Assert the data grid container is visible."""
        expect(self.page.locator(self.DATA_GRID).first).to_be_visible()

    def expect_grid_has_data(self) -> None:
        """Assert the grid contains at least one data row."""
        expect(self.page.locator(self.GRID_ROWS)).not_to_have_count(0)

    def is_grid_empty(self) -> bool:
        """Return True if the grid has no data rows."""
        return self.get_row_count() == 0
