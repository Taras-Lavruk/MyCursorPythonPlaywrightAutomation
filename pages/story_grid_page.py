"""
StoryGridPage — Jira Align Stories data grid.

URL pattern: /StoryGrid?Portfolios={id}&Releases={id}

The Stories page has a different sidebar structure ("More items" menu)
compared to the Epic grid.

Inherits:
  BasePage → HeaderPage → SidebarPage → GridPage → StoryGridPage
"""

import logging
import re

from playwright.sync_api import Page, expect

from pages.grid_page import GridPage

_logger = logging.getLogger(__name__)


class StoryGridPage(GridPage):
    """Page object for the Stories grid page."""

    # ── Sidebar navigation (scoped to aside to avoid header collisions) ────────
    SIDEBAR_BACK_TO_MENU = "aside button:has-text('Back to'), aside a:has-text('Back to previous menu')"
    SIDEBAR_THEMES = "aside a:has-text('Themes')"
    SIDEBAR_CAPABILITIES = "aside a:has-text('Capabilities')"
    SIDEBAR_FEATURES = "aside a:has-text('Features')"
    SIDEBAR_STORIES = "aside a:has-text('Stories')"
    SIDEBAR_DEPENDENCIES = "aside a:has-text('Dependencies')"
    SIDEBAR_WORK_ITEM_LINKS = "aside a:has-text('Work Item Links')"

    # ── Story grid columns ─────────────────────────────────────────────────────
    COLUMN_ID = "th:has-text('ID')"
    COLUMN_EXT_ID = "th:has-text('Ext ID')"
    COLUMN_STORY = "th:has-text('Story')"
    COLUMN_STATE = "th:has-text('State')"
    COLUMN_SPRINT = "th:has-text('Sprint')"
    COLUMN_HOURS = "th:has-text('Hours')"
    COLUMN_CREATED_BY = "th:has-text('Created By')"

    # ── Story-specific action buttons ──────────────────────────────────────────
    QUICK_ADD_STORY = "button:has-text('Quick Add Story')"
    ESTIMATION_BUTTON = "button:has-text('Estimation')"
    IMPORT_STORIES_BUTTON = "button:has-text('Import Stories'), button:has-text('Import')"
    IMPORT_CRITERIA_BUTTON = "button:has-text('Import Criteria')"
    MASS_EDIT_BUTTON = "button:has-text('Mass Edit')"
    STORY_CARDS_BUTTON = "button:has-text('Story Cards')"

    # ── Quick add form ─────────────────────────────────────────────────────────
    QUICK_ADD_TITLE_INPUT = "input[placeholder*='title' i], input[name*='title' i]"
    QUICK_ADD_SAVE_BUTTON = "button:has-text('Save'), button[type='submit']"
    QUICK_ADD_CANCEL_BUTTON = "button:has-text('Cancel')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Sidebar navigation ─────────────────────────────────────────────────────

    def click_back_to_previous_menu(self) -> None:
        """Navigate back to the previous menu in sidebar."""
        btn = self.page.locator(self.SIDEBAR_BACK_TO_MENU).first
        if btn.is_visible(timeout=0):
            btn.click()

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

    # ── Story-specific actions ─────────────────────────────────────────────────

    def quick_add_story(self, title: str | None = None) -> None:
        """Open quick-add story dialog, optionally pre-filling the title."""
        self.page.locator(self.QUICK_ADD_STORY).click()
        self._logger.debug("Quick-add story dialog opened")
        if title is not None:
            self.page.locator(self.QUICK_ADD_TITLE_INPUT).fill(title)

    def save_quick_add_story(self) -> None:
        """Save the story from the quick-add dialog."""
        self.page.locator(self.QUICK_ADD_SAVE_BUTTON).click()

    def cancel_quick_add_story(self) -> None:
        """Cancel the quick-add story dialog."""
        self.page.locator(self.QUICK_ADD_CANCEL_BUTTON).click()

    def open_estimation(self) -> None:
        """Open story estimation dialog."""
        btn = self.page.locator(self.ESTIMATION_BUTTON).first
        if btn.is_visible(timeout=0):
            btn.click()

    def import_stories(self) -> None:
        """Open import stories dialog."""
        btn = self.page.locator(self.IMPORT_STORIES_BUTTON).first
        if btn.is_visible(timeout=0):
            btn.click()

    def import_criteria(self) -> None:
        """Open import acceptance criteria dialog."""
        btn = self.page.locator(self.IMPORT_CRITERIA_BUTTON).first
        if btn.is_visible(timeout=0):
            btn.click()

    def open_mass_edit(self) -> None:
        """Open mass edit dialog for stories."""
        btn = self.page.locator(self.MASS_EDIT_BUTTON).first
        if btn.is_visible(timeout=0):
            btn.click()

    def print_story_cards(self) -> None:
        """Print story cards."""
        btn = self.page.locator(self.STORY_CARDS_BUTTON).first
        if btn.is_visible(timeout=0):
            btn.click()

    # ── Data accessors ─────────────────────────────────────────────────────────

    def get_story_ids(self) -> list[str]:
        """Return all story IDs from the first table column."""
        return self.page.locator("table tbody td:first-child").all_inner_texts()

    def search_story_by_title(self, title: str) -> None:
        """Search for a story by title using the grid search box."""
        self.search_grid(title)

    def get_story_count(self) -> int:
        """Return the number of stories currently visible in the grid."""
        return self.get_row_count()

    def filter_by_sprint(self, sprint_name: str) -> None:
        """Filter stories by sprint name using the grid search box."""
        self.search_grid(sprint_name)

    # ── Assertions ─────────────────────────────────────────────────────────────

    def expect_story_grid_loaded(self) -> None:
        """Assert the story grid URL, grid, and header are all present."""
        expect(self.page).to_have_url(re.compile(r"/StoryGrid", re.IGNORECASE))
        self.expect_grid_visible()
        self.expect_header_visible()

    def expect_story_columns_visible(self) -> None:
        """Assert the core story columns (ID, Story, State) are visible."""
        expect(self.page.locator(self.COLUMN_ID)).to_be_visible()
        expect(self.page.locator(self.COLUMN_STORY)).to_be_visible()
        expect(self.page.locator(self.COLUMN_STATE)).to_be_visible()

    def expect_quick_add_visible(self) -> None:
        """Assert the quick-add story button is visible."""
        expect(self.page.locator(self.QUICK_ADD_STORY)).to_be_visible()
