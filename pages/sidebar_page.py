from playwright.sync_api import Page, expect
from pages.header_page import HeaderPage


class SidebarPage(HeaderPage):
    """Base class for pages with a left navigation sidebar.
    
    Portfolio Room, Grid pages (Epics, Stories, etc.) have left sidebars
    with context-specific navigation.
    """

    # Sidebar Container
    SIDEBAR_CONTAINER = "[class*='sidebar'], aside, [role='navigation']:not(header)"
    SIDEBAR_TOGGLE_BUTTON = "button[aria-label*='sidebar' i], button[title*='sidebar' i]"
    
    # Common Sidebar Elements
    SIDEBAR_LINKS = "[class*='sidebar'] a, aside a"
    SIDEBAR_ACTIVE_LINK = "[class*='sidebar'] a[class*='active'], aside a[class*='active']"
    
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def is_sidebar_visible(self) -> bool:
        """Check if the left sidebar is visible."""
        return self.page.locator(self.SIDEBAR_CONTAINER).count() > 0 and \
               self.page.locator(self.SIDEBAR_CONTAINER).first.is_visible()

    def toggle_sidebar(self) -> None:
        """Toggle the sidebar visibility if toggle button exists."""
        if self.page.locator(self.SIDEBAR_TOGGLE_BUTTON).count() > 0:
            self.page.locator(self.SIDEBAR_TOGGLE_BUTTON).click()

    def get_sidebar_links(self) -> list[str]:
        """Get all link texts from the sidebar."""
        if not self.is_sidebar_visible():
            return []
        return self.page.locator(self.SIDEBAR_LINKS).all_inner_texts()

    def get_active_sidebar_link(self) -> str:
        """Get the text of the currently active sidebar link."""
        if self.page.locator(self.SIDEBAR_ACTIVE_LINK).count() > 0:
            return self.page.locator(self.SIDEBAR_ACTIVE_LINK).first.inner_text()
        return ""

    def expect_sidebar_visible(self) -> None:
        """Verify the sidebar is visible."""
        expect(self.page.locator(self.SIDEBAR_CONTAINER).first).to_be_visible()
