# Page Object Model Architecture

## Visual Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│ BasePage                                                     │
│ • Core Playwright functionality                             │
│ • navigate(), get_url(), wait_for_load()                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
┌────────▼─────────┐    ┌─────────▼──────────────────────────┐
│ LoginPage        │    │ HeaderPage                          │
│ • /login         │    │ • Top navigation (ALL pages)        │
│ • No header      │    │ • Logo, menus, profile              │
│ • login()        │    │ • click_home(), click_logout()      │
└──────────────────┘    └─────────┬───────────────────────────┘
                                  │
                      ┌───────────┴───────────┐
                      │                       │
            ┌─────────▼───────────┐  ┌───────▼────────────────┐
            │ HomePage            │  │ SidebarPage            │
            │ • /default          │  │ • Pages with sidebar   │
            │ • No sidebar        │  │ • is_sidebar_visible() │
            │ • Recent rooms      │  │ • get_sidebar_links()  │
            │ • Starred items     │  └───────┬────────────────┘
            └─────────────────────┘          │
                                   ┌─────────▼────────────────┐
                                   │ GridPage                 │
                                   │ • Data grid pages        │
                                   │ • search_grid()          │
                                   │ • get_row_count()        │
                                   │ • Pagination             │
                                   └─────────┬────────────────┘
                                             │
                       ┌─────────────────────┼─────────────────────┐
                       │                     │                     │
              ┌────────▼──────────┐  ┌──────▼────────────┐  ┌────▼──────┐
              │ EpicGridPage      │  │ StoryGridPage     │  │ ...       │
              │ • /EpicGrid       │  │ • /StoryGrid      │  │           │
              │ • Epic sidebar    │  │ • Story sidebar   │  │           │
              │ • quick_add_epic()│  │ • quick_add_story()  │           │
              └───────────────────┘  └───────────────────┘  └───────────┘
```

## Method Availability Matrix

| Method                    | Base | Header | Sidebar | Grid | Home | Epic | Story |
|--------------------------|------|--------|---------|------|------|------|-------|
| `navigate()`             | ✅   | ✅     | ✅      | ✅   | ✅   | ✅   | ✅    |
| `get_url()`              | ✅   | ✅     | ✅      | ✅   | ✅   | ✅   | ✅    |
| `click_home()`           | ❌   | ✅     | ✅      | ✅   | ✅   | ✅   | ✅    |
| `click_logout()`         | ❌   | ✅     | ✅      | ✅   | ✅   | ✅   | ✅    |
| `navigate_to_epics()`    | ❌   | ✅     | ✅      | ✅   | ✅   | ✅   | ✅    |
| `is_sidebar_visible()`   | ❌   | ❌     | ✅      | ✅   | ❌   | ✅   | ✅    |
| `search_grid()`          | ❌   | ❌     | ❌      | ✅   | ❌   | ✅   | ✅    |
| `get_row_count()`        | ❌   | ❌     | ❌      | ✅   | ❌   | ✅   | ✅    |
| `is_recent_rooms_visible()` | ❌   | ❌     | ❌      | ❌   | ✅   | ❌   | ❌    |
| `quick_add_epic()`       | ❌   | ❌     | ❌      | ❌   | ❌   | ✅   | ❌    |
| `quick_add_story()`      | ❌   | ❌     | ❌      | ❌   | ❌   | ❌   | ✅    |

## File Structure

```
pages/
├── __init__.py                 # Exports all page classes
├── README.md                   # Detailed documentation
├── ARCHITECTURE.md             # This file
├── base_page.py               # BasePage - Foundation
├── header_page.py             # HeaderPage - Shared navigation
├── sidebar_page.py            # SidebarPage - Left sidebar
├── grid_page.py               # GridPage - Data grids
├── login_page.py              # LoginPage - Authentication
├── home_page.py               # HomePage - Dashboard
├── epic_grid_page.py          # EpicGridPage - Epics
└── story_grid_page.py         # StoryGridPage - Stories
```

## Design Patterns Used

### 1. Page Object Pattern
Each page/component is represented by a class with locators and methods.

### 2. Inheritance Hierarchy
Common functionality moves up the inheritance chain to avoid duplication.

### 3. Composition Over Repetition
- HeaderPage contains all navigation → inherited by pages that need it
- SidebarPage contains sidebar logic → inherited by pages with sidebars
- GridPage contains grid operations → inherited by all grid pages

### 4. Single Responsibility
- **BasePage**: Playwright wrapper
- **HeaderPage**: Navigation header only
- **SidebarPage**: Left sidebar only
- **GridPage**: Data grid operations only
- **Specific pages**: Page-specific features only

## Real-World Usage Flow

### Scenario: User logs in and creates an epic

```python
# Step 1: Login (LoginPage - no header)
login_page = LoginPage(page)
login_page.open()
login_page.login(username, password)

# Step 2: On Home (HomePage - has header, no sidebar)
home_page = HomePage(page)
home_page.expect_home_sections_visible()

# Step 3: Navigate to Epics (using HeaderPage method)
home_page.navigate_to_epics()

# Step 4: On Epic Grid (EpicGridPage - has header, sidebar, grid)
epic_page = EpicGridPage(page)
epic_page.expect_epic_grid_loaded()  # Specific validation

# Use inherited methods from different levels:
epic_page.quick_add_epic()           # EpicGridPage specific
epic_page.search_grid("API")         # GridPage inherited
epic_page.navigate_to_backlog()      # EpicGridPage sidebar
epic_page.click_logout()             # HeaderPage inherited
```

## Key Benefits

### ✅ Code Reusability
- Header navigation written once, used everywhere
- Grid operations shared across all grid pages
- No duplication of common functionality

### ✅ Maintainability
- Change header locator once → affects all pages
- Update grid search logic once → all grids benefit
- Clear separation of concerns

### ✅ Scalability
- Add new grid page: extend GridPage, define only unique features
- Add new page with header: extend HeaderPage
- Add new page without header: extend BasePage

### ✅ Type Safety & IDE Support
- Clear inheritance chain
- Autocomplete shows all available methods
- Easy to discover what a page can do

### ✅ Test Readability
```python
# Clear what's happening at each step
home_page.navigate_to_epics()    # Navigation
epic_page.search_grid("test")     # Grid operation
epic_page.navigate_to_backlog()   # Sidebar navigation
epic_page.click_logout()          # Header action
```

## Comparison: Before vs After

### Before (Flat Structure)
```python
# home_page.py - 200 lines
class HomePage:
    # Everything: navigation, profile, content, etc.
    LOGO = "..."
    HOME_BUTTON = "..."
    PROFILE_BUTTON = "..."
    RECENT_ROOMS = "..."
    # ... all methods ...

# epic_page.py - 250 lines
class EpicPage:
    # Duplicate: navigation, profile, sidebar, grid, epic-specific
    LOGO = "..."  # Duplicate!
    HOME_BUTTON = "..."  # Duplicate!
    PROFILE_BUTTON = "..."  # Duplicate!
    SIDEBAR = "..."
    GRID = "..."
    # ... all methods duplicated ...

# story_page.py - 250 lines
class StoryPage:
    # More duplicates!
    LOGO = "..."  # Duplicate!
    HOME_BUTTON = "..."  # Duplicate!
    # ... more duplication ...
```

### After (Hierarchical Structure)
```python
# header_page.py - 150 lines (shared)
class HeaderPage:
    LOGO = "..."
    HOME_BUTTON = "..."
    PROFILE_BUTTON = "..."
    # Shared navigation methods

# grid_page.py - 100 lines (shared)
class GridPage(SidebarPage):
    # Shared grid methods

# epic_grid_page.py - 60 lines (unique only!)
class EpicGridPage(GridPage):
    # ONLY epic-specific features
    EPIC_COLUMNS = "..."
    quick_add_epic()

# story_grid_page.py - 70 lines (unique only!)
class StoryGridPage(GridPage):
    # ONLY story-specific features
    STORY_COLUMNS = "..."
    quick_add_story()
```

**Result:** 
- Less code overall
- No duplication
- Easier to maintain
- Clearer responsibilities

## Extension Guide

### Adding a new grid page (e.g., FeatureGridPage)

```python
from pages.grid_page import GridPage

class FeatureGridPage(GridPage):
    """Features grid page."""
    
    # Only define what's unique to features
    COLUMN_FEATURE_NAME = "th:has-text('Feature')"
    ADD_FEATURE_BUTTON = "button:has-text('Add Feature')"
    
    def add_feature(self, name: str) -> None:
        self.click_add()  # Inherited from GridPage
        # Feature-specific logic here
        
    def expect_feature_grid_loaded(self) -> None:
        expect(self.page).to_have_url_contains("/FeatureGrid")
        self.expect_grid_visible()  # Inherited
```

That's it! You get:
- ✅ All header navigation (from HeaderPage)
- ✅ Sidebar support (from SidebarPage)
- ✅ Grid operations (from GridPage)
- ✅ Only need to define feature-specific items

---

**Created:** April 2026  
**Based on:** Live analysis of Jira Align application  
**Pattern:** Page Object Model with Inheritance Hierarchy
