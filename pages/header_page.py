from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class HeaderPage(BasePage):
    """Shared header/navigation elements present on ALL pages in Jira Align.
    
    This class should be the base for all page objects as the header is consistent
    across the entire application.
    """

    # Logo
    LOGO = ".jira-align-logo, header img[alt*='Jira Align' i]"
    
    # Top Navigation - Main Menu Buttons
    HOME_BUTTON = "button:has-text('Home')"
    TEAMS_DROPDOWN = "button:has-text('Teams')"
    PRODUCT_DROPDOWN = "button:has-text('Product')"
    CUSTOM_ROOMS_DROPDOWN = "button:has-text('Custom Rooms')"
    STARRED_DROPDOWN = "button:has-text('Starred')"
    ITEMS_DROPDOWN = "button:has-text('Items')"
    CREATE_BUTTON = "button:has-text('Create')"
    
    # Right Toolbar Buttons
    SEARCH_BUTTON = "button[aria-label*='search' i], header button[title*='search' i]"
    NOTIFICATIONS_BUTTON = "button[aria-label*='notification' i], header button[title*='notification' i]"
    HELP_BUTTON = "button[aria-label*='help' i], header button[title*='help' i]"
    SETTINGS_BUTTON = "button[aria-label*='setting' i], header button[title*='setting' i], button:has-text('Settings'), [data-testid*='settings' i], [data-test-id*='settings' i], a[href*='admin' i], header button:has([class*='gear' i]), header button:has([class*='cog' i])"
    PROFILE_BUTTON = "button:has-text('Profile'), header button:last-child, [data-testid*='profile' i]"
    
    # Settings Dropdown Menu Items  
    SETTINGS_MENU_ADMINISTRATION = "a:has-text('Administration'), a:has-text('Admin Settings'), a:has-text('Admin'), a[href*='admin' i], a[href*='administration' i], button:has-text('Administration'), [role='menuitem']:has-text('Administration'), [role='menuitem']:has-text('Admin')"
    
    # Profile Dropdown Menu Items
    PROFILE_MENU_ABOUT = "a:has-text('About')"
    PROFILE_MENU_HELP = "a:has-text('Help')"
    PROFILE_MENU_SUPPORT = "a:has-text('Support')"
    PROFILE_MENU_SETTINGS = "a:has-text('Personal Settings')"
    PROFILE_MENU_PROFILE = "a:has-text('Profile')"
    PROFILE_MENU_IMPERSONATE = "a:has-text('Impersonate')"
    PROFILE_MENU_LOGOUT = "a:has-text('Logout')"
    
    # Items Dropdown Submenu
    ITEMS_MENU_THEME = "a:has-text('Theme')"
    ITEMS_MENU_EPIC = "a:has-text('Epic')"
    ITEMS_MENU_CAPABILITY = "a:has-text('Capability')"
    ITEMS_MENU_FEATURE = "a:has-text('Feature')"
    ITEMS_MENU_STORY = "a:has-text('Story')"
    ITEMS_MENU_DEFECTS = "a:has-text('Defects')"
    ITEMS_MENU_TASKS = "a:has-text('Tasks')"
    ITEMS_MENU_OBJECTIVES = "a:has-text('Objectives')"
    ITEMS_MENU_DEPENDENCIES = "a:has-text('Dependencies')"
    ITEMS_MENU_IDEATION = "a:has-text('Ideation')"
    ITEMS_MENU_RISKS = "a:has-text('Risks')"
    ITEMS_MENU_IMPEDIMENTS = "a:has-text('Impediments')"
    ITEMS_MENU_SPRINTS = "a:has-text('Sprints')"
    ITEMS_MENU_RELEASES = "a:has-text('Releases')"
    
    # Navigation Structure
    HEADER_NAV = "nav, header"
    
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Logo Actions
    def click_logo(self) -> None:
        """Click the Jira Align logo to return to home."""
        self.page.locator(self.LOGO).click()

    def is_logo_visible(self) -> bool:
        """Check if logo is visible."""
        return self.page.locator(self.LOGO).is_visible()

    # Main Navigation Actions
    def click_home(self) -> None:
        """Navigate to Home page."""
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
        """Click the Create button (primary action)."""
        self.page.locator(self.CREATE_BUTTON).click()

    # Navigate to Specific Item Types
    def navigate_to_epics(self) -> None:
        """Navigate to Epics grid page via Items menu."""
        self.open_items_dropdown()
        self.page.locator(self.ITEMS_MENU_EPIC).click()

    def navigate_to_stories(self) -> None:
        """Navigate to Stories grid page via Items menu."""
        self.open_items_dropdown()
        self.page.locator(self.ITEMS_MENU_STORY).click()

    def navigate_to_features(self) -> None:
        """Navigate to Features grid page via Items menu."""
        self.open_items_dropdown()
        self.page.locator(self.ITEMS_MENU_FEATURE).click()

    def navigate_to_defects(self) -> None:
        """Navigate to Defects grid page via Items menu."""
        self.open_items_dropdown()
        self.page.locator(self.ITEMS_MENU_DEFECTS).click()

    # Right Toolbar Actions
    def click_search(self) -> None:
        """Open search functionality."""
        self.page.locator(self.SEARCH_BUTTON).click()

    def click_notifications(self) -> None:
        """Open notifications panel."""
        self.page.locator(self.NOTIFICATIONS_BUTTON).click()

    def click_help(self) -> None:
        """Open help menu."""
        self.page.locator(self.HELP_BUTTON).click()

    def click_settings(self) -> None:
        """Open settings menu/dropdown."""
        self.page.locator(self.SETTINGS_BUTTON).click()

    def navigate_to_administration(self) -> None:
        """Navigate to Administration page via settings menu or direct URL."""
        # Strategy 1: Try clicking settings button and menu item
        try:
            settings_button = self.page.locator(self.SETTINGS_BUTTON)
            if settings_button.count() > 0 and settings_button.first.is_visible(timeout=3000):
                settings_button.first.click()
                self.page.wait_for_timeout(1000)  # Wait for dropdown to appear
                
                # Look for administration menu item
                admin_link = self.page.locator(self.SETTINGS_MENU_ADMINISTRATION)
                if admin_link.count() > 0 and admin_link.first.is_visible(timeout=3000):
                    admin_link.first.click()
                    self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                    return
        except Exception as e:
            print(f"Settings button navigation failed: {e}")
        
        # Strategy 2: Try direct URL navigation
        try:
            from config.settings import settings
            admin_url = f"{settings.BASE_URL.rstrip('/')}/administration"
            print(f"Trying direct navigation to: {admin_url}")
            self.page.goto(admin_url)
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            return
        except Exception as e:
            print(f"Direct URL navigation failed: {e}")
        
        # Strategy 3: Look for any admin link visible on current page
        try:
            admin_links = self.page.locator("a[href*='admin' i], a:has-text('Administration')")
            if admin_links.count() > 0:
                print(f"Found {admin_links.count()} admin links on page")
                admin_links.first.click()
                self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                return
        except Exception as e:
            print(f"Admin link search failed: {e}")
        
        raise Exception("Failed to navigate to Administration page using all strategies")

    # Profile Menu Actions
    def open_profile_menu(self) -> None:
        """Open the user profile dropdown menu."""
        self.page.locator(self.PROFILE_BUTTON).click()

    def click_logout(self) -> None:
        """Logout from the authenticated session."""
        self.open_profile_menu()
        self.page.locator(self.PROFILE_MENU_LOGOUT).click()

    def click_personal_settings(self) -> None:
        """Navigate to personal settings from profile menu."""
        self.open_profile_menu()
        self.page.locator(self.PROFILE_MENU_SETTINGS).click()

    def click_help_from_profile(self) -> None:
        """Open help from profile menu."""
        self.open_profile_menu()
        self.page.locator(self.PROFILE_MENU_HELP).click()

    # Validation Methods
    def expect_header_visible(self) -> None:
        """Verify the header navigation is visible."""
        expect(self.page.locator(self.HEADER_NAV)).to_be_visible()
        expect(self.page.locator(self.HOME_BUTTON)).to_be_visible()
        expect(self.page.locator(self.PROFILE_BUTTON)).to_be_visible()

    def expect_authenticated(self) -> None:
        """Verify user is authenticated (profile button visible)."""
        expect(self.page.locator(self.PROFILE_BUTTON)).to_be_visible()
        assert "login" not in self.page.url.lower(), "Should not be on login page"

    def is_profile_button_visible(self) -> bool:
        """Check if profile button is visible (indicates authentication)."""
        return self.page.locator(self.PROFILE_BUTTON).is_visible()
