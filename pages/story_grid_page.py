from playwright.sync_api import Page, expect
from pages.grid_page import GridPage


class StoryGridPage(GridPage):
    """Page object for the Stories grid page.
    
    URL pattern: /StoryGrid?Portfolios={id}&Releases={id}
    
    The Stories page has a different sidebar structure ("More items" menu)
    compared to the Epic grid.
    """

    # Story-Specific Sidebar Links (More Items menu)
    SIDEBAR_BACK_TO_MENU = "button:has-text('Back to'), a:has-text('Back to previous menu')"
    SIDEBAR_THEMES = "a:has-text('Themes')"
    SIDEBAR_CAPABILITIES = "a:has-text('Capabilities')"
    SIDEBAR_FEATURES = "a:has-text('Features')"
    SIDEBAR_STORIES = "a:has-text('Stories')"
    SIDEBAR_DEPENDENCIES = "a:has-text('Dependencies')"
    SIDEBAR_WORK_ITEM_LINKS = "a:has-text('Work Item Links')"
    
    # Story Grid Columns
    COLUMN_ID = "th:has-text('ID')"
    COLUMN_EXT_ID = "th:has-text('Ext ID')"
    COLUMN_STORY = "th:has-text('Story')"
    COLUMN_STATE = "th:has-text('State')"
    COLUMN_SPRINT = "th:has-text('Sprint')"
    COLUMN_HOURS = "th:has-text('Hours')"
    COLUMN_CREATED_BY = "th:has-text('Created By')"
    
    # Story-Specific Action Buttons
    QUICK_ADD_STORY = "button:has-text('Quick Add Story')"
    ESTIMATION_BUTTON = "button:has-text('Estimation')"
    IMPORT_STORIES_BUTTON = "button:has-text('Import Stories'), button:has-text('Import')"
    IMPORT_CRITERIA_BUTTON = "button:has-text('Import Criteria')"
    MASS_EDIT_BUTTON = "button:has-text('Mass Edit')"
    STORY_CARDS_BUTTON = "button:has-text('Story Cards')"
    
    # Quick Add Form (when visible)
    QUICK_ADD_TITLE_INPUT = "input[placeholder*='title' i], input[name*='title' i]"
    QUICK_ADD_SAVE_BUTTON = "button:has-text('Save'), button[type='submit']"
    QUICK_ADD_CANCEL_BUTTON = "button:has-text('Cancel')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Sidebar Navigation
    def click_back_to_previous_menu(self) -> None:
        """Navigate back to the previous menu in sidebar."""
        if self.page.locator(self.SIDEBAR_BACK_TO_MENU).count() > 0:
            self.page.locator(self.SIDEBAR_BACK_TO_MENU).first.click()

    def navigate_to_themes(self) -> None:
        """Navigate to Themes from sidebar."""
        self.page.locator(self.SIDEBAR_THEMES).click()

    def navigate_to_capabilities(self) -> None:
        """Navigate to Capabilities from sidebar."""
        self.page.locator(self.SIDEBAR_CAPABILITIES).click()

    def navigate_to_features(self) -> None:
        """Navigate to Features from sidebar."""
        self.page.locator(self.SIDEBAR_FEATURES).click()

    def navigate_to_dependencies(self) -> None:
        """Navigate to Dependencies from sidebar."""
        self.page.locator(self.SIDEBAR_DEPENDENCIES).click()

    # Story-Specific Actions
    def quick_add_story(self, title: str = None) -> None:
        """Open quick add story dialog, optionally with title."""
        self.page.locator(self.QUICK_ADD_STORY).click()
        if title:
            self.page.locator(self.QUICK_ADD_TITLE_INPUT).fill(title)

    def save_quick_add_story(self) -> None:
        """Save the story from quick add dialog."""
        self.page.locator(self.QUICK_ADD_SAVE_BUTTON).click()

    def cancel_quick_add_story(self) -> None:
        """Cancel the quick add story dialog."""
        self.page.locator(self.QUICK_ADD_CANCEL_BUTTON).click()

    def open_estimation(self) -> None:
        """Open story estimation dialog."""
        if self.page.locator(self.ESTIMATION_BUTTON).count() > 0:
            self.page.locator(self.ESTIMATION_BUTTON).click()

    def import_stories(self) -> None:
        """Open import stories dialog."""
        if self.page.locator(self.IMPORT_STORIES_BUTTON).count() > 0:
            self.page.locator(self.IMPORT_STORIES_BUTTON).first.click()

    def import_criteria(self) -> None:
        """Open import acceptance criteria dialog."""
        if self.page.locator(self.IMPORT_CRITERIA_BUTTON).count() > 0:
            self.page.locator(self.IMPORT_CRITERIA_BUTTON).click()

    def open_mass_edit(self) -> None:
        """Open mass edit dialog for stories."""
        if self.page.locator(self.MASS_EDIT_BUTTON).count() > 0:
            self.page.locator(self.MASS_EDIT_BUTTON).click()

    def print_story_cards(self) -> None:
        """Print story cards."""
        if self.page.locator(self.STORY_CARDS_BUTTON).count() > 0:
            self.page.locator(self.STORY_CARDS_BUTTON).click()

    # Story Grid Queries
    def get_story_ids(self) -> list[str]:
        """Get all story IDs from the ID column."""
        id_cells = self.page.locator("table tbody td:first-child")
        return id_cells.all_inner_texts()

    def search_story_by_title(self, title: str) -> None:
        """Search for a story by title."""
        self.search_grid(title)

    def get_story_count(self) -> int:
        """Get the count of stories in the grid."""
        return self.get_row_count()

    def filter_by_sprint(self, sprint_name: str) -> None:
        """Filter stories by sprint name."""
        self.search_grid(sprint_name)

    # Validation
    def expect_story_grid_loaded(self) -> None:
        """Verify the story grid page is loaded."""
        expect(self.page).to_have_url_contains("/StoryGrid")
        self.expect_grid_visible()
        self.expect_header_visible()

    def expect_story_columns_visible(self) -> None:
        """Verify key story columns are visible."""
        expect(self.page.locator(self.COLUMN_ID)).to_be_visible()
        expect(self.page.locator(self.COLUMN_STORY)).to_be_visible()
        expect(self.page.locator(self.COLUMN_STATE)).to_be_visible()

    def expect_quick_add_visible(self) -> None:
        """Verify quick add story button is visible."""
        expect(self.page.locator(self.QUICK_ADD_STORY)).to_be_visible()
