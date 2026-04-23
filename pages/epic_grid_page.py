from playwright.sync_api import Page, expect
from pages.grid_page import GridPage


class EpicGridPage(GridPage):
    """Page object for the Epics grid page.
    
    URL pattern: /EpicGrid?Portfolios={id}&Releases={id}&FilterID={id}
    
    Inherits header navigation from HeaderPage, sidebar from SidebarPage,
    and common grid functionality from GridPage.
    """

    # Epic-Specific Sidebar Links
    SIDEBAR_PORTFOLIO_ROOM = "a:has-text('Portfolio-FC Room')"
    SIDEBAR_EPICS = "a:has-text('Epics')"
    SIDEBAR_BACKLOG = "a:has-text('Backlog')"
    SIDEBAR_ROADMAPS = "a:has-text('Roadmaps')"
    SIDEBAR_OKR_HUB = "a:has-text('OKR hub')"
    SIDEBAR_WORK_TREE = "a:has-text('Work tree')"
    SIDEBAR_FORECAST = "a:has-text('Forecast')"
    SIDEBAR_CAPACITY = "a:has-text('Capacity')"
    
    # Epic Grid Columns
    COLUMN_ID = "th:has-text('ID')"
    COLUMN_EXT_ID = "th:has-text('Ext ID')"
    COLUMN_TITLE = "th:has-text('Title')"
    COLUMN_STATE = "th:has-text('State')"
    COLUMN_OWNER = "th:has-text('Owner')"
    COLUMN_TAGS = "th:has-text('Tags')"
    
    # Epic-Specific Action Buttons
    IMPORT_EPICS_BUTTON = "button:has-text('Import'), a:has-text('Import Epics')"
    EXPORT_EPICS_BUTTON = "button:has-text('Export'), a:has-text('Export Epics')"
    BOTTOM_UP_ESTIMATE_BUTTON = "button:has-text('Bottom-Up Estimate')"
    PRINT_EPIC_CARDS_BUTTON = "button:has-text('Print Epic Cards')"
    
    # Quick Add
    QUICK_ADD_EPIC = "button:has-text('Quick Add'), button:has-text('Add Epic')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Sidebar Navigation
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

    # Epic-Specific Actions
    def quick_add_epic(self) -> None:
        """Open quick add epic dialog."""
        if self.page.locator(self.QUICK_ADD_EPIC).count() > 0:
            self.page.locator(self.QUICK_ADD_EPIC).first.click()

    def import_epics(self) -> None:
        """Open import epics dialog."""
        if self.page.locator(self.IMPORT_EPICS_BUTTON).count() > 0:
            self.page.locator(self.IMPORT_EPICS_BUTTON).first.click()

    def export_epics(self) -> None:
        """Export epics to file."""
        if self.page.locator(self.EXPORT_EPICS_BUTTON).count() > 0:
            self.page.locator(self.EXPORT_EPICS_BUTTON).first.click()

    def open_bottom_up_estimate(self) -> None:
        """Open bottom-up estimation dialog."""
        if self.page.locator(self.BOTTOM_UP_ESTIMATE_BUTTON).count() > 0:
            self.page.locator(self.BOTTOM_UP_ESTIMATE_BUTTON).click()

    def print_epic_cards(self) -> None:
        """Print epic cards."""
        if self.page.locator(self.PRINT_EPIC_CARDS_BUTTON).count() > 0:
            self.page.locator(self.PRINT_EPIC_CARDS_BUTTON).click()

    # Epic Grid Queries
    def get_epic_ids(self) -> list[str]:
        """Get all epic IDs from the ID column."""
        id_cells = self.page.locator("table tbody td:first-child")
        return id_cells.all_inner_texts()

    def search_epic_by_title(self, title: str) -> None:
        """Search for an epic by title."""
        self.search_grid(title)

    def get_epic_count(self) -> int:
        """Get the count of epics in the grid."""
        return self.get_row_count()

    # Validation
    def expect_epic_grid_loaded(self) -> None:
        """Verify the epic grid page is loaded."""
        expect(self.page).to_have_url_contains("/EpicGrid")
        self.expect_grid_visible()
        self.expect_header_visible()
        self.expect_sidebar_visible()

    def expect_epic_columns_visible(self) -> None:
        """Verify key epic columns are visible."""
        expect(self.page.locator(self.COLUMN_ID)).to_be_visible()
        expect(self.page.locator(self.COLUMN_TITLE)).to_be_visible()
        expect(self.page.locator(self.COLUMN_STATE)).to_be_visible()
