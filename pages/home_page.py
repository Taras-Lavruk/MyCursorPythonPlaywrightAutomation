from playwright.sync_api import Page, expect
from pages.header_page import HeaderPage


class HomePage(HeaderPage):
    """Page object for the authenticated Jira Align home page.
    
    Note: This page requires authentication. Users must log in first and will be 
    redirected to this page. Do not navigate directly to this page without logging in.
    
    URL after login: https://rc-manual.jiraalign.xyz/default?FirstTime=True
    
    The home page has NO left sidebar, only the top navigation header.
    """
    
    # Alert Banner
    ALERT_BANNER = "[role='alert']"
    ALERT_CLOSE_BUTTON = "[role='alert'] button"
    
    # Main Content Sections
    RECENT_ROOMS_HEADING = "h3:has-text('Recent rooms')"
    STARRED_HEADING = "h3:has-text('Starred')"
    STARRED_VIEW_ALL = "a:has-text('View all')"
    
    # Content Cards (Portfolios, Programs, Teams)
    PORTFOLIO_CARDS = ".card, [class*='portfolio'], [class*='card']"
    CARD_TITLES = "[class*='card'] h4, [class*='card'] h3"
    
    # Main Content Area
    MAIN_CONTENT = "main, [role='main']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Alert Banner Actions
    def dismiss_alert_banner(self) -> None:
        """Dismiss the alert banner if present."""
        if self.page.locator(self.ALERT_BANNER).count() > 0:
            self.page.locator(self.ALERT_CLOSE_BUTTON).click()

    def get_alert_message(self) -> str:
        """Get the alert banner message text."""
        return self.page.locator(self.ALERT_BANNER).inner_text()

    # Content Section Methods
    def is_recent_rooms_visible(self) -> bool:
        """Check if Recent rooms section is visible."""
        return self.page.locator(self.RECENT_ROOMS_HEADING).is_visible()

    def is_starred_section_visible(self) -> bool:
        """Check if Starred section is visible."""
        return self.page.locator(self.STARRED_HEADING).is_visible()

    def get_portfolio_cards_count(self) -> int:
        """Get count of portfolio/program cards displayed."""
        return self.page.locator(self.PORTFOLIO_CARDS).count()

    def get_card_titles(self) -> list[str]:
        """Get titles of all portfolio/program cards."""
        return self.page.locator(self.CARD_TITLES).all_inner_texts()

    def click_portfolio_card(self, title: str) -> None:
        """Click a portfolio/program card by its title."""
        self.page.locator(f"{self.CARD_TITLES}:has-text('{title}')").first.click()

    def click_view_all_starred(self) -> None:
        """Click 'View all' link in Starred section."""
        self.page.locator(self.STARRED_VIEW_ALL).click()

    # Page State Validations
    def expect_loaded(self) -> None:
        """Verify the home page is loaded after successful login."""
        expect(self.page).to_have_title("Jira Align")
        self.wait_for_load()
        self.expect_header_visible()

    def expect_main_content_visible(self) -> None:
        """Verify main content area is visible."""
        expect(self.page.locator(self.MAIN_CONTENT).first).to_be_visible()

    def expect_home_sections_visible(self) -> None:
        """Verify key home page sections are visible."""
        expect(self.page.locator(self.RECENT_ROOMS_HEADING)).to_be_visible()
        expect(self.page.locator(self.STARRED_HEADING)).to_be_visible()
