# Playwright MCP Guide for Test Creation

## Overview

This project uses the Playwright MCP (Model Context Protocol) to help create tests and find correct locators for web elements. The MCP provides tools for browser automation, inspection, and code generation.

## Available MCP Tools

The Playwright MCP server provides the following tools:

### Navigation & Interaction
- `playwright_navigate` - Navigate to a URL
- `playwright_click` - Click on elements
- `playwright_fill` - Fill form inputs
- `playwright_hover` - Hover over elements
- `playwright_select` - Select dropdown options
- `playwright_press_key` - Press keyboard keys
- `playwright_drag` - Drag and drop elements

### Inspection & Debugging
- `playwright_get_visible_html` - Get HTML content of the page
- `playwright_get_visible_text` - Get visible text from the page
- `playwright_screenshot` - Take screenshots
- `playwright_console_logs` - Get browser console logs

### Code Generation
- `start_codegen_session` - Start recording actions to generate test code
- `get_codegen_session` - Get information about a codegen session
- `end_codegen_session` - Stop recording and get generated code
- `clear_codegen_session` - Clear the current session

### HTTP Testing
- `playwright_get`, `playwright_post`, `playwright_put`, `playwright_patch`, `playwright_delete` - Make HTTP requests
- `playwright_expect_response` - Wait for and validate responses
- `playwright_assert_response` - Assert response properties

### Advanced Features
- `playwright_iframe_click`, `playwright_iframe_fill` - Interact with iframes
- `playwright_upload_file` - Upload files
- `playwright_evaluate` - Execute JavaScript in the page context
- `playwright_resize` - Resize viewport
- `playwright_go_back`, `playwright_go_forward` - Browser navigation
- `playwright_click_and_switch_tab` - Handle new tabs

## How to Find Correct Locators

### Method 1: Manual Inspection Script

Use the included inspection script to analyze a page and find the best locators:

```bash
python3 inspect_login_page.py
```

This script will:
1. Navigate to the target page
2. Take a screenshot
3. Save the HTML content
4. Inspect all form elements and print their attributes
5. Identify the best selectors for each element

### Method 2: Using Playwright MCP Tools Directly

1. **Navigate to the page:**
   ```python
   # Via MCP tool
   playwright_navigate(url="https://your-app.com/login")
   ```

2. **Get the HTML content:**
   ```python
   # Via MCP tool
   playwright_get_visible_html(selector="form")  # Get form HTML only
   ```

3. **Take a screenshot for visual reference:**
   ```python
   # Via MCP tool
   playwright_screenshot(name="login_form", fullPage=True)
   ```

4. **Inspect the HTML to find:**
   - IDs (prefer these when available)
   - Name attributes
   - Data-testid attributes
   - Specific classes
   - Semantic role attributes

### Method 3: Code Generation Session

Use Playwright's built-in codegen to record interactions:

```python
# Start a codegen session
start_codegen_session(options={
    "outputPath": "/path/to/output",
    "testNamePrefix": "Login",
    "includeComments": True
})

# Perform manual interactions in the browser
# The MCP will record your actions

# Get the generated code
get_codegen_session(sessionId="session-id")

# End the session
end_codegen_session(sessionId="session-id")
```

## Best Practices for Locators

### Priority Order (most to least stable):

1. **IDs** - `#elementId`
   - Most stable if IDs are semantic and don't change
   - Example: `#sso_id`, `#btnLogin`

2. **Data-testid attributes** - `[data-testid='login-button']`
   - Specifically added for testing
   - Very stable

3. **Name attributes** - `input[name='username']`
   - Commonly used in forms
   - Relatively stable

4. **Semantic selectors** - `button[type='submit']`
   - Based on element meaning
   - Moderately stable

5. **Text content** - `button:has-text('Sign In')`
   - Can break with text changes or i18n
   - Use for unique elements only

6. **Classes** - `.login-button`
   - Can change with styling updates
   - Less stable, avoid if possible

7. **CSS paths** - `div.container > form > button:nth-child(3)`
   - Most fragile
   - Breaks easily with DOM changes
   - Avoid unless necessary

### Example: Login Page Locators

Based on MCP inspection of `https://rc-manual.jiraalign.xyz/login`:

```python
# ✅ GOOD - Specific, stable locators found via MCP
USERNAME_INPUT = "#sso_id"  # ID selector
PASSWORD_INPUT = "#sso_password"  # ID selector
SUBMIT_BUTTON = "#btnLogin"  # ID selector

# ❌ BAD - Generic fallback selectors
USERNAME_INPUT = "input[name='username'], input[type='email'], #username, #email"
PASSWORD_INPUT = "input[name='password'], input[type='password'], #password"
SUBMIT_BUTTON = "button[type='submit'], input[type='submit']"
```

## Workflow for Creating New Tests

1. **Inspect the page first:**
   ```bash
   # Modify inspect_login_page.py for your target page
   # Or use MCP tools to navigate and inspect
   ```

2. **Document findings:**
   - Take screenshots
   - Save HTML for reference
   - Note element attributes

3. **Create Page Object:**
   ```python
   class MyPage(BasePage):
       # Use specific locators found via MCP
       ELEMENT = "#specific-id"  # Not generic selectors
   ```

4. **Write tests:**
   ```python
   def test_feature(self, page: Page):
       my_page = MyPage(page)
       my_page.interact_with_element()
   ```

5. **Validate:**
   - Run tests to ensure locators work
   - Check for flakiness
   - Update if elements change

## Common Issues and Solutions

### Issue: "Element not found"
**Solution:** Use MCP to inspect the actual page and verify:
- Element exists when test runs
- Correct timing (wait for element to appear)
- No iframes involved (use `playwright_iframe_*` tools)

### Issue: "Selector matches multiple elements"
**Solution:** Make selector more specific:
- Add parent context: `form #submit-button`
- Use first(): `page.locator("button").first`
- Find unique attribute via MCP inspection

### Issue: "Tests work locally but fail in CI"
**Solution:**
- Check timing: add proper waits
- Verify viewport size: use `playwright_resize`
- Check browser version compatibility

## Resources

- MCP Tools Directory: `~/.cursor/projects/<project>/mcps/user-Playwright/tools/`
- Tool Schemas: Each tool has a JSON descriptor with parameters
- Playwright Docs: https://playwright.dev/python/docs/intro

## Tips

1. Always inspect the actual page before creating tests
2. Prefer stable locators (IDs, data-testid) over brittle ones (classes, nth-child)
3. Use the MCP screenshot tool to capture the state when debugging
4. Keep locators DRY by centralizing them in Page Objects
5. Document why you chose specific locators if they're non-obvious
