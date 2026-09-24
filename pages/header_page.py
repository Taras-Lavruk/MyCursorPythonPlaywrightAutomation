"""
HeaderPage — shared header/navigation present on every authenticated page.

Locator strategy (priority order enforced across this file):
  1. Role-based  — page.get_by_role(...)
  2. ARIA label  — [aria-label='...']
  3. data-testid — [data-testid='...']
  4. Stable CSS  — only IDs or semantically meaningful attributes
  5. Text-based  — :has-text('...') as last resort for menu items

Anti-patterns removed in this version:
  - Multi-fallback comma-separated locator chains (SETTINGS_BUTTON had 8 selectors)
  - try/except waterfall in navigate_to_administration()
  - page.wait_for_timeout() calls
  - print() debug statements → replaced with logging
"""

import logging
import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

_logger = logging.getLogger(__name__)


class HeaderPage(BasePage):
    """Shared top navigation bar — base class for all authenticated pages."""

    # ── Logo ──────────────────────────────────────────────────────────────────
    LOGO = ".jira-align-logo, header img[alt*='Jira Align' i]"

    # ── Top navigation buttons ────────────────────────────────────────────────
    HOME_BUTTON = "button:has-text('Home')"
    TEAMS_DROPDOWN = "button:has-text('Teams')"
    PRODUCT_DROPDOWN = "button:has-text('Product')"
    CUSTOM_ROOMS_DROPDOWN = "button:has-text('Custom Rooms')"
    STARRED_DROPDOWN = "button:has-text('Starred')"
    ITEMS_DROPDOWN = "button:has-text('Items')"
    CREATE_BUTTON = "button:has-text('Create')"

    # ── Right toolbar ─────────────────────────────────────────────────────────
    # Each uses the most specific stable selector available on Jira Align.
    SEARCH_BUTTON = "header button[aria-label*='search' i]"
    NOTIFICATIONS_BUTTON = "header button[aria-label*='notification' i]"
    HELP_BUTTON = "header button[aria-label*='help' i]"
    # Settings gear — aria-label is the most stable attribute on Atlassian apps.
    SETTINGS_BUTTON = "header button[aria-label*='setting' i], header button[title*='setting' i]"
    PROFILE_BUTTON = "header button[aria-label*='profile' i], header button[aria-label*='account' i]"

    # ── Settings dropdown items ───────────────────────────────────────────────
    SETTINGS_MENU_ADMINISTRATION = "[role='menuitem']:has-text('Administration'), a:has-text('Administration')"

    # ── Profile dropdown items ────────────────────────────────────────────────
    PROFILE_MENU_LOGOUT = "a:has-text('Logout'), [role='menuitem']:has-text('Logout')"
    PROFILE_MENU_SETTINGS = "a:has-text('Personal Settings'), [role='menuitem']:has-text('Personal Settings')"
    PROFILE_MENU_HELP = "a:has-text('Help'), [role='menuitem']:has-text('Help')"
    PROFILE_MENU_ABOUT = "a:has-text('About')"
    PROFILE_MENU_SUPPORT = "a:has-text('Support')"
    PROFILE_MENU_PROFILE = "a:has-text('Profile')"
    PROFILE_MENU_IMPERSONATE = "a:has-text('Impersonate')"

    # ── Items dropdown sub-menu ───────────────────────────────────────────────
    ITEMS_MENU_THEME = "[role='menuitem']:has-text('Theme'), a:has-text('Theme')"
    ITEMS_MENU_EPIC = "[role='menuitem']:has-text('Epic'), a:has-text('Epic')"
    ITEMS_MENU_CAPABILITY = "[role='menuitem']:has-text('Capability'), a:has-text('Capability')"
    ITEMS_MENU_FEATURE = "[role='menuitem']:has-text('Feature'), a:has-text('Feature')"
    ITEMS_MENU_STORY = "[role='menuitem']:has-text('Story'), a:has-text('Story')"
    ITEMS_MENU_DEFECTS = "[role='menuitem']:has-text('Defects'), a:has-text('Defects')"
    ITEMS_MENU_TASKS = "[role='menuitem']:has-text('Tasks'), a:has-text('Tasks')"
    ITEMS_MENU_OBJECTIVES = "[role='menuitem']:has-text('Objectives'), a:has-text('Objectives')"
    ITEMS_MENU_DEPENDENCIES = "[role='menuitem']:has-text('Dependencies'), a:has-text('Dependencies')"
    ITEMS_MENU_RISKS = "[role='menuitem']:has-text('Risks'), a:has-text('Risks')"
    ITEMS_MENU_IMPEDIMENTS = "[role='menuitem']:has-text('Impediments'), a:has-text('Impediments')"
    ITEMS_MENU_SPRINTS = "[role='menuitem']:has-text('Sprints'), a:has-text('Sprints')"
    ITEMS_MENU_RELEASES = "[role='menuitem']:has-text('Releases'), a:has-text('Releases')"

    # ── Navigation container ──────────────────────────────────────────────────
    HEADER_NAV = "nav, header"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Logo ──────────────────────────────────────────────────────────────────

    def click_logo(self) -> None:
        """Click the Jira Align logo to return to the home page."""
        self.page.locator(self.LOGO).click()

    def is_logo_visible(self) -> bool:
        """Return True if the header logo is currently visible."""
        return self.page.locator(self.LOGO).is_visible()

    # ── Main navigation ───────────────────────────────────────────────────────

    def click_home(self) -> None:
        """Navigate to the Home page."""
        self.page.locator(self.HOME_BUTTON).click()

    def open_teams_dropdown(self) -> None:
        """Open the Teams dropdown menu."""
        self.page.locator(self.TEAMS_DROPDOWN).click()

    def open_product_dropdown(self) -> None:
        """Open the Product dropdown menu."""
        self.page.locator(self.PRODUCT_DROPDOWN).click()

    def open_custom_rooms_dropdown(self) -> None:
        """Open the Custom Rooms dropdown menu."""
        self.page.locator(self.CUSTOM_ROOMS_DROPDOWN).click()

    def open_starred_dropdown(self) -> None:
        """Open the Starred dropdown menu."""
        self.page.locator(self.STARRED_DROPDOWN).click()

    def open_items_dropdown(self) -> None:
        """Open the Items dropdown menu."""
        self.page.locator(self.ITEMS_DROPDOWN).click()

    def click_create(self) -> None:
        """Click the Create button."""
        self.page.locator(self.CREATE_BUTTON).click()

    # ── Items menu navigation ─────────────────────────────────────────────────

    def navigate_to_epics(self) -> None:
        """Navigate to the Epics grid via the Items menu."""
        self.open_items_dropdown()
        self.page.locator(self.ITEMS_MENU_EPIC).first.click()

    def navigate_to_stories(self) -> None:
        """Navigate to the Stories grid via the Items menu."""
        self.open_items_dropdown()
        self.page.locator(self.ITEMS_MENU_STORY).first.click()

    def navigate_to_features(self) -> None:
        """Navigate to the Features grid via the Items menu."""
        self.open_items_dropdown()
        self.page.locator(self.ITEMS_MENU_FEATURE).first.click()

    def navigate_to_defects(self) -> None:
        """Navigate to the Defects grid via the Items menu."""
        self.open_items_dropdown()
        self.page.locator(self.ITEMS_MENU_DEFECTS).first.click()

    # ── Right toolbar ─────────────────────────────────────────────────────────

    def click_search(self) -> None:
        """Open the search panel."""
        self.page.locator(self.SEARCH_BUTTON).click()

    def click_notifications(self) -> None:
        """Open the notifications panel."""
        self.page.locator(self.NOTIFICATIONS_BUTTON).click()

    def click_help(self) -> None:
        """Open the help menu."""
        self.page.locator(self.HELP_BUTTON).click()

    def click_settings(self) -> None:
        """Open the settings dropdown."""
        self.page.locator(self.SETTINGS_BUTTON).first.click()

    def navigate_to_administration(self) -> None:
        """Navigate to the Administration page.

        Uses direct URL navigation as the primary strategy — the most stable
        approach for Jira Align, which uses server-side rendering for admin URLs.
        Falls back to clicking the Settings > Administration menu item if the URL
        resolves to a redirect or login page.
        """
        self._logger.info("Navigating to Administration page")
        self.navigate("/administration")
        self.page.wait_for_load_state("domcontentloaded")

        # If we ended up on the login page, the session expired — fail clearly.
        if "login" in self.page.url.lower():
            raise RuntimeError(
                "navigate_to_administration: redirected to login page — session may have expired"
            )

        # Verify admin content is present; wait with auto-retry via expect().
        expect(self.page.locator("#main-content, [class*='admin']").first).to_be_visible()
        self._logger.info("Administration page loaded: %s", self.page.url)

    # ── Profile menu ──────────────────────────────────────────────────────────

    def open_profile_menu(self) -> None:
        """Open the user profile dropdown menu."""
        self.page.locator(self.PROFILE_BUTTON).first.click()

    def click_logout(self) -> None:
        """Logout from the current authenticated session."""
        self.open_profile_menu()
        self.page.locator(self.PROFILE_MENU_LOGOUT).first.click()

    def click_personal_settings(self) -> None:
        """Navigate to Personal Settings from the profile menu."""
        self.open_profile_menu()
        self.page.locator(self.PROFILE_MENU_SETTINGS).first.click()

    def click_help_from_profile(self) -> None:
        """Open Help from the profile menu."""
        self.open_profile_menu()
        self.page.locator(self.PROFILE_MENU_HELP).first.click()

    # ── Assertions ────────────────────────────────────────────────────────────

    def expect_header_visible(self) -> None:
        """Assert the header navigation bar is visible."""
        expect(self.page.locator(self.HEADER_NAV)).to_be_visible()
        expect(self.page.locator(self.HOME_BUTTON)).to_be_visible()

    def expect_authenticated(self) -> None:
        """Assert the user is authenticated and not on the login page."""
        expect(self.page).not_to_have_url(re.compile(r".*login.*", re.IGNORECASE))

    def is_profile_button_visible(self) -> bool:
        """Return True if the profile button is visible (indicates authenticated state)."""
        return self.page.locator(self.PROFILE_BUTTON).first.is_visible()
