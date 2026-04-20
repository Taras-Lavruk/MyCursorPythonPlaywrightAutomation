"""Temporary script to inspect login page and find correct locators."""
from playwright.sync_api import sync_playwright
from config.settings import settings

def inspect_login_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        
        # Navigate to login page
        login_url = f"{settings.BASE_URL.rstrip('/')}/login"
        print(f"Navigating to: {login_url}")
        page.goto(login_url)
        page.wait_for_load_state("networkidle")
        
        # Take a screenshot
        page.screenshot(path="login_page.png", full_page=True)
        print("Screenshot saved as login_page.png")
        
        # Get the page HTML
        html_content = page.content()
        
        # Save HTML to file
        with open("login_page_html.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("HTML saved as login_page_html.html")
        
        # Try to find login form elements
        print("\n=== Inspecting Form Elements ===\n")
        
        # Look for username/email inputs
        print("Looking for username/email input...")
        username_selectors = [
            "input[name='username']",
            "input[name='email']",
            "input[type='email']",
            "input[placeholder*='email' i]",
            "input[placeholder*='username' i]",
            "input[id='username']",
            "input[id='email']",
            "#username",
            "#email"
        ]
        
        for selector in username_selectors:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    attrs = {
                        "id": element.get_attribute("id"),
                        "name": element.get_attribute("name"),
                        "type": element.get_attribute("type"),
                        "placeholder": element.get_attribute("placeholder"),
                        "class": element.get_attribute("class"),
                        "data-testid": element.get_attribute("data-testid"),
                    }
                    print(f"✓ Found with selector: {selector}")
                    print(f"  Attributes: {attrs}")
                    break
            except Exception as e:
                continue
        
        # Look for password inputs
        print("\nLooking for password input...")
        password_selectors = [
            "input[type='password']",
            "input[name='password']",
            "input[placeholder*='password' i]",
            "#password"
        ]
        
        for selector in password_selectors:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    attrs = {
                        "id": element.get_attribute("id"),
                        "name": element.get_attribute("name"),
                        "type": element.get_attribute("type"),
                        "placeholder": element.get_attribute("placeholder"),
                        "class": element.get_attribute("class"),
                        "data-testid": element.get_attribute("data-testid"),
                    }
                    print(f"✓ Found with selector: {selector}")
                    print(f"  Attributes: {attrs}")
                    break
            except Exception as e:
                continue
        
        # Look for submit buttons
        print("\nLooking for submit button...")
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Sign In')",
            "button:has-text('Login')",
            "button:has-text('Log In')",
            "[data-testid='login-button']",
            "[data-testid='submit-button']"
        ]
        
        for selector in submit_selectors:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    attrs = {
                        "id": element.get_attribute("id"),
                        "name": element.get_attribute("name"),
                        "type": element.get_attribute("type"),
                        "class": element.get_attribute("class"),
                        "data-testid": element.get_attribute("data-testid"),
                        "text": element.text_content()
                    }
                    print(f"✓ Found with selector: {selector}")
                    print(f"  Attributes: {attrs}")
                    break
            except Exception as e:
                continue
        
        # Print all input elements for reference
        print("\n=== All Input Elements on Page ===\n")
        inputs = page.locator("input").all()
        for i, inp in enumerate(inputs):
            attrs = {
                "id": inp.get_attribute("id"),
                "name": inp.get_attribute("name"),
                "type": inp.get_attribute("type"),
                "placeholder": inp.get_attribute("placeholder"),
                "class": inp.get_attribute("class"),
            }
            print(f"{i+1}. {attrs}")
        
        print("\n=== All Button Elements on Page ===\n")
        buttons = page.locator("button").all()
        for i, btn in enumerate(buttons):
            attrs = {
                "id": btn.get_attribute("id"),
                "name": btn.get_attribute("name"),
                "type": btn.get_attribute("type"),
                "class": btn.get_attribute("class"),
                "text": btn.text_content()
            }
            print(f"{i+1}. {attrs}")
        
        # Keep browser open for inspection
        print("\nBrowser will stay open for 10 seconds for manual inspection...")
        page.wait_for_timeout(10000)
        
        browser.close()

if __name__ == "__main__":
    inspect_login_page()
