from playwright.sync_api import Page, expect
from pages.sidebar_page import SidebarPage


class GridPage(SidebarPage):
    """Base class for data grid pages (Epics, Stories, Features, etc.).
    
    All grid pages share common functionality: search, filters, pagination,
    column configuration, and action toolbars.
    """

    # Search and Filters
    SEARCH_BOX = "input[type='search'], input[placeholder*='search' i]"
    FILTER_BUTTON = "button:has-text('Filter'), button[title*='filter' i]"
    CONFIGURATION_BAR = "[class*='config'], [class*='toolbar']"
    
    # Action Toolbar
    MORE_ACTIONS_DROPDOWN = "button:has-text('More Actions'), button:has-text('Actions')"
    STAR_PAGE_BUTTON = "button:has-text('Star Page')"
    SHARE_BUTTON = "button:has-text('Share')"
    EXPORT_BUTTON = "button:has-text('Export')"
    
    # Data Grid
    DATA_GRID = "table, [role='grid'], [class*='grid']"
    GRID_ROWS = "table tbody tr, [role='row']"
    GRID_HEADERS = "table thead th, [role='columnheader']"
    COLUMN_SELECTOR = "button:has-text('Columns'), button:has-text('Select Columns')"
    
    # Pagination
    PAGINATION_CONTAINER = "[class*='pagination'], .pagination"
    FIRST_PAGE_BUTTON = "button:has-text('First'), button[title*='First' i]"
    PREVIOUS_PAGE_BUTTON = "button:has-text('Previous'), button[title*='Previous' i]"
    NEXT_PAGE_BUTTON = "button:has-text('Next'), button[title*='Next' i]"
    LAST_PAGE_BUTTON = "button:has-text('Last'), button[title*='Last' i]"
    PAGE_INFO = "[class*='page-info'], .page-info"
    
    # Common Grid Actions
    ADD_BUTTON = "button:has-text('Add'), button[title*='Add' i]"
    REFRESH_BUTTON = "button:has-text('Refresh'), button[title*='Refresh' i]"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Search and Filter Actions
    def search_grid(self, query: str) -> None:
        """Search within the grid."""
        if self.page.locator(self.SEARCH_BOX).count() > 0:
            self.page.locator(self.SEARCH_BOX).fill(query)
            self.page.keyboard.press("Enter")

    def clear_search(self) -> None:
        """Clear the search box."""
        if self.page.locator(self.SEARCH_BOX).count() > 0:
            self.page.locator(self.SEARCH_BOX).fill("")

    def open_filters(self) -> None:
        """Open the filter panel."""
        if self.page.locator(self.FILTER_BUTTON).count() > 0:
            self.page.locator(self.FILTER_BUTTON).click()

    # Toolbar Actions
    def open_more_actions(self) -> None:
        """Open the More Actions dropdown menu."""
        self.page.locator(self.MORE_ACTIONS_DROPDOWN).click()

    def star_page(self) -> None:
        """Star/favorite the current page."""
        if self.page.locator(self.STAR_PAGE_BUTTON).count() > 0:
            self.page.locator(self.STAR_PAGE_BUTTON).click()

    def click_share(self) -> None:
        """Click the Share button."""
        if self.page.locator(self.SHARE_BUTTON).count() > 0:
            self.page.locator(self.SHARE_BUTTON).click()

    def click_export(self) -> None:
        """Export grid data."""
        if self.page.locator(self.EXPORT_BUTTON).count() > 0:
            self.page.locator(self.EXPORT_BUTTON).click()

    # Grid Data Methods
    def get_row_count(self) -> int:
        """Get the number of visible rows in the grid."""
        return self.page.locator(self.GRID_ROWS).count()

    def get_column_headers(self) -> list[str]:
        """Get all column header texts."""
        return self.page.locator(self.GRID_HEADERS).all_inner_texts()

    def open_column_selector(self) -> None:
        """Open the column selector to show/hide columns."""
        if self.page.locator(self.COLUMN_SELECTOR).count() > 0:
            self.page.locator(self.COLUMN_SELECTOR).click()

    # Pagination Methods
    def go_to_first_page(self) -> None:
        """Navigate to the first page of results."""
        if self.page.locator(self.FIRST_PAGE_BUTTON).count() > 0:
            self.page.locator(self.FIRST_PAGE_BUTTON).click()

    def go_to_previous_page(self) -> None:
        """Navigate to the previous page of results."""
        if self.page.locator(self.PREVIOUS_PAGE_BUTTON).count() > 0:
            self.page.locator(self.PREVIOUS_PAGE_BUTTON).click()

    def go_to_next_page(self) -> None:
        """Navigate to the next page of results."""
        if self.page.locator(self.NEXT_PAGE_BUTTON).count() > 0:
            self.page.locator(self.NEXT_PAGE_BUTTON).click()

    def go_to_last_page(self) -> None:
        """Navigate to the last page of results."""
        if self.page.locator(self.LAST_PAGE_BUTTON).count() > 0:
            self.page.locator(self.LAST_PAGE_BUTTON).click()

    def get_page_info(self) -> str:
        """Get pagination information (e.g., 'Showing 1-20 of 100')."""
        if self.page.locator(self.PAGE_INFO).count() > 0:
            return self.page.locator(self.PAGE_INFO).inner_text()
        return ""

    # Common Actions
    def click_add(self) -> None:
        """Click the Add button to create a new item."""
        if self.page.locator(self.ADD_BUTTON).count() > 0:
            self.page.locator(self.ADD_BUTTON).click()

    def refresh_grid(self) -> None:
        """Refresh the grid data."""
        if self.page.locator(self.REFRESH_BUTTON).count() > 0:
            self.page.locator(self.REFRESH_BUTTON).click()

    # Validation Methods
    def expect_grid_visible(self) -> None:
        """Verify the data grid is visible."""
        expect(self.page.locator(self.DATA_GRID).first).to_be_visible()

    def expect_grid_has_data(self) -> None:
        """Verify the grid contains at least one row of data."""
        expect(self.page.locator(self.GRID_ROWS)).to_have_count_greater_than(0)

    def is_grid_empty(self) -> bool:
        """Check if the grid has no data rows."""
        return self.get_row_count() == 0
