# Page Object Model Structure

This directory contains page objects for the Jira Align application, organized in a hierarchical structure based on shared functionality.

## Inheritance Hierarchy

```
BasePage (base_page.py)
│
├── LoginPage (login_page.py)
│
└── HeaderPage (header_page.py) - Shared navigation header
    │
    ├── HomePage (home_page.py) - Dashboard with no sidebar
    │
    └── SidebarPage (sidebar_page.py) - Pages with left sidebar
        │
        └── GridPage (grid_page.py) - Data grid pages
            │
            ├── EpicGridPage (epic_grid_page.py)
            ├── StoryGridPage (story_grid_page.py)
            └── ... (other grid pages)
```

## Page Object Classes

### Base Classes

#### `BasePage`
Foundation class with core Playwright functionality.
- Navigation methods
- Timeout configuration
- Screenshot utilities
- Element interaction helpers

**Used by:** All page objects

---

#### `HeaderPage` (extends `BasePage`)
Shared top navigation header present on **ALL authenticated pages**.

**Locators:**
- Logo
- Main navigation: Home, Teams, Product, Custom Rooms, Starred, Items, Create
- Right toolbar: Search, Notifications, Help, Settings, Profile
- Profile dropdown menu items
- Items dropdown submenu

**Methods:**
```python
click_home()
open_items_dropdown()
navigate_to_epics()
navigate_to_stories()
click_logout()
open_profile_menu()
expect_header_visible()
expect_authenticated()
```

**Used by:** HomePage, SidebarPage (and all pages that have headers)

---

#### `SidebarPage` (extends `HeaderPage`)
Base class for pages with a left navigation sidebar.

**Locators:**
- Sidebar container
- Sidebar toggle button
- Sidebar links

**Methods:**
```python
is_sidebar_visible()
toggle_sidebar()
get_sidebar_links()
get_active_sidebar_link()
expect_sidebar_visible()
```

**Used by:** GridPage, Portfolio Room pages, Team pages

---

#### `GridPage` (extends `SidebarPage`)
Base class for data grid pages (Epics, Stories, Features, etc.).

**Locators:**
- Search box and filters
- Action toolbar (More Actions, Star, Share, Export)
- Data grid and columns
- Pagination controls
- Add/Refresh buttons

**Methods:**
```python
search_grid(query)
open_filters()
open_more_actions()
star_page()
get_row_count()
get_column_headers()
go_to_next_page()
expect_grid_visible()
expect_grid_has_data()
```

**Used by:** EpicGridPage, StoryGridPage, FeatureGridPage, etc.

---

### Specific Page Classes

#### `LoginPage` (extends `BasePage`)
Login/authentication page.

**URL:** `/login`

**Locators:**
- Username input: `#sso_id`
- Password input: `#sso_password`
- Submit button: `#btnLogin`
- Error messages

**Methods:**
```python
open()
login(username, password)
get_error_message()
expect_login_form_visible()
```

---

#### `HomePage` (extends `HeaderPage`)
Main dashboard page after login. **No sidebar.**

**URL:** `/default?FirstTime=True`

**Unique Locators:**
- Alert banner
- Recent rooms section
- Starred section
- Portfolio/Program cards

**Methods:**
```python
dismiss_alert_banner()
is_recent_rooms_visible()
get_portfolio_cards_count()
get_card_titles()
click_portfolio_card(title)
expect_home_sections_visible()
```

**Inherits from HeaderPage:**
- All navigation methods
- Profile menu actions
- Logout functionality

---

#### `EpicGridPage` (extends `GridPage`)
Epics data grid page.

**URL:** `/EpicGrid?Portfolios={id}&Releases={id}&FilterID={id}`

**Unique Locators:**
- Epic-specific sidebar links (Portfolio Room, Backlog, Roadmaps, OKR hub, Work tree, Forecast, Capacity)
- Epic grid columns (ID, Ext ID, Title, State, Owner, Tags)
- Epic actions (Import/Export, Bottom-Up Estimate, Print Epic Cards)

**Methods:**
```python
navigate_to_backlog()
navigate_to_roadmaps()
quick_add_epic()
import_epics()
get_epic_ids()
search_epic_by_title(title)
expect_epic_grid_loaded()
```

**Inherits from GridPage:**
- Search, filter, pagination
- Grid data methods
- Common action toolbar

**Inherits from SidebarPage:**
- Sidebar visibility checks
- Sidebar navigation

**Inherits from HeaderPage:**
- Top navigation
- Profile menu
- Logout

---

#### `StoryGridPage` (extends `GridPage`)
Stories data grid page.

**URL:** `/StoryGrid?Portfolios={id}&Releases={id}`

**Unique Locators:**
- Different sidebar structure ("More items" menu with Back button)
- Story-specific sidebar links (Themes, Capabilities, Features, Stories, Dependencies)
- Story grid columns (ID, Ext ID, Story, State, Sprint, Hours, Created By)
- Story actions (Quick Add Story, Estimation, Mass Edit, Story Cards)

**Methods:**
```python
click_back_to_previous_menu()
navigate_to_features()
quick_add_story(title)
save_quick_add_story()
open_estimation()
import_stories()
open_mass_edit()
get_story_ids()
expect_story_grid_loaded()
```

**Inherits from GridPage:**
- All grid functionality
- Plus sidebar and header functionality

---

## Usage Examples

### Example 1: Login and Navigate to Epics

```python
from pages import LoginPage, EpicGridPage

def test_navigate_to_epics(page):
    # Login
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("user@test.com", "password")
    
    # Navigate to Epics via header
    epic_page = EpicGridPage(page)
    epic_page.navigate_to_epics()  # From HeaderPage
    
    # Verify grid loaded
    epic_page.expect_epic_grid_loaded()
    
    # Search for epic
    epic_page.search_grid("API Integration")
    
    # Get results
    count = epic_page.get_row_count()
    print(f"Found {count} epics")
```

### Example 2: Using Inherited Methods

```python
from pages import StoryGridPage

def test_story_workflow(page, logged_in_page):
    story_page = StoryGridPage(page)
    
    # Navigate using HeaderPage method
    story_page.navigate_to_stories()
    
    # Use GridPage methods
    story_page.search_grid("User authentication")
    story_page.expect_grid_has_data()
    
    # Use StoryGridPage specific method
    story_page.quick_add_story("New story title")
    story_page.save_quick_add_story()
    
    # Use HeaderPage method to logout
    story_page.click_logout()
```

### Example 3: Home Page with Header Actions

```python
from pages import LoginPage, HomePage

def test_home_page_navigation(page):
    # Login
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("user@test.com", "password")
    
    # On home page
    home_page = HomePage(page)
    home_page.expect_home_sections_visible()
    
    # Use HomePage specific methods
    cards = home_page.get_card_titles()
    home_page.click_portfolio_card(cards[0])
    
    # Use HeaderPage inherited methods
    home_page.click_home()  # Navigate back
    home_page.open_profile_menu()
    home_page.click_logout()
```

## Key Design Principles

### 1. **DRY (Don't Repeat Yourself)**
Common functionality is in base classes. Each page only defines what's unique to it.

### 2. **Single Responsibility**
- `BasePage`: Core Playwright functionality
- `HeaderPage`: Top navigation (shared across ALL pages)
- `SidebarPage`: Left sidebar functionality
- `GridPage`: Data grid functionality
- Specific pages: Unique features only

### 3. **Inheritance Chain**
Each page inherits all methods from its parent classes:
- `EpicGridPage` → `GridPage` → `SidebarPage` → `HeaderPage` → `BasePage`
- Access to all methods from all parent classes

### 4. **Explicit Over Implicit**
- Clear method names: `navigate_to_epics()` not just `to_epics()`
- Descriptive locators: `SIDEBAR_PORTFOLIO_ROOM` not just `ROOM_LINK`

### 5. **Validation Methods**
Each page has `expect_*` methods to verify page state:
- `expect_loaded()`
- `expect_grid_visible()`
- `expect_sidebar_visible()`

## Adding New Page Objects

### For a new grid page (e.g., Features):

```python
from pages.grid_page import GridPage

class FeatureGridPage(GridPage):
    """Feature-specific grid page."""
    
    # Define ONLY feature-specific locators
    COLUMN_FEATURE_NAME = "th:has-text('Feature')"
    ADD_FEATURE_BUTTON = "button:has-text('Add Feature')"
    
    def __init__(self, page: Page) -> None:
        super().__init__(page)
    
    # Define ONLY feature-specific methods
    def add_feature(self, name: str) -> None:
        self.click_add()  # Inherited from GridPage
        # Feature-specific add logic
        
    def expect_feature_grid_loaded(self) -> None:
        expect(self.page).to_have_url_contains("/FeatureGrid")
        self.expect_grid_visible()  # Inherited
```

### For a non-grid page with sidebar:

```python
from pages.sidebar_page import SidebarPage

class PortfolioRoomPage(SidebarPage):
    """Portfolio room dashboard page."""
    
    # Define portfolio-specific locators
    FINANCIALS_BUTTON = "button:has-text('Financials')"
    RESOURCES_BUTTON = "button:has-text('Resources')"
    
    # Portfolio-specific methods
    def click_financials(self) -> None:
        self.page.locator(self.FINANCIALS_BUTTON).click()
```

## Testing the Page Objects

See `tests/e2e/` directory for example tests using these page objects.

## Maintenance

When adding new locators or methods:

1. **Determine the right level:** Does it belong in a base class or specific page?
2. **Check for duplicates:** Is this functionality already in a parent class?
3. **Update this README:** Document new pages and significant changes
4. **Update `__init__.py`:** Export new page classes

---

**Last Updated:** Based on live analysis of Jira Align application (April 2026)
