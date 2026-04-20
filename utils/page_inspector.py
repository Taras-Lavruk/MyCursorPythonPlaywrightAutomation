"""
Utility to inspect web pages and find correct locators using Playwright.
This tool helps you find the most reliable selectors for your Page Objects.

Usage:
    python3 -m utils.page_inspector --url https://example.com/page --selector "form"
    python3 -m utils.page_inspector --path /login --selector ".login-form"
"""

import argparse
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, Locator
from config.settings import settings


class PageInspector:
    """Inspects web pages and suggests optimal locators."""
    
    def __init__(self, url: str, headless: bool = False):
        self.url = url
        self.headless = headless
        self.page = None
        self.browser = None
        self.context = None
    
    def start(self):
        """Launch browser and navigate to URL."""
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        self.page = self.context.new_page()
        
        print(f"🌐 Navigating to: {self.url}")
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")
        print("✅ Page loaded successfully\n")
    
    def take_screenshot(self, filename: str = "page_screenshot.png") -> str:
        """Take a full-page screenshot."""
        self.page.screenshot(path=filename, full_page=True)
        print(f"📸 Screenshot saved: {filename}")
        return filename
    
    def save_html(self, filename: str = "page_source.html") -> str:
        """Save the page HTML."""
        html = self.page.content()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"💾 HTML saved: {filename}")
        return filename
    
    def get_element_attributes(self, locator: Locator) -> dict:
        """Extract all useful attributes from an element."""
        if locator.count() == 0:
            return {}
        
        element = locator.first
        return {
            "id": element.get_attribute("id"),
            "name": element.get_attribute("name"),
            "type": element.get_attribute("type"),
            "class": element.get_attribute("class"),
            "placeholder": element.get_attribute("placeholder"),
            "aria-label": element.get_attribute("aria-label"),
            "data-testid": element.get_attribute("data-testid"),
            "role": element.get_attribute("role"),
            "value": element.get_attribute("value"),
        }
    
    def suggest_locator(self, attributes: dict) -> str:
        """Suggest the best locator based on available attributes."""
        # Priority order for stable locators
        if attributes.get("data-testid"):
            return f"[data-testid='{attributes['data-testid']}']"
        if attributes.get("id"):
            return f"#{attributes['id']}"
        if attributes.get("name"):
            return f"[name='{attributes['name']}']"
        if attributes.get("aria-label"):
            return f"[aria-label='{attributes['aria-label']}']"
        if attributes.get("type"):
            return f"[type='{attributes['type']}']"
        
        return "❌ No stable locator found - consider adding data-testid or id"
    
    def inspect_inputs(self) -> list:
        """Find and analyze all input elements."""
        print("🔍 Inspecting input elements...\n")
        inputs = self.page.locator("input").all()
        results = []
        
        for i, inp in enumerate(inputs, 1):
            attrs = self.get_element_attributes(inp)
            suggested_locator = self.suggest_locator(attrs)
            
            print(f"Input #{i}:")
            print(f"  Suggested locator: {suggested_locator}")
            print(f"  Attributes: {attrs}\n")
            
            results.append({
                "type": "input",
                "index": i,
                "attributes": attrs,
                "suggested_locator": suggested_locator
            })
        
        return results
    
    def inspect_buttons(self) -> list:
        """Find and analyze all button elements."""
        print("🔍 Inspecting button elements...\n")
        buttons = self.page.locator("button").all()
        results = []
        
        for i, btn in enumerate(buttons, 1):
            attrs = self.get_element_attributes(btn)
            text = btn.text_content().strip()
            attrs["text"] = text
            
            suggested_locator = self.suggest_locator(attrs)
            if suggested_locator.startswith("❌") and text:
                suggested_locator = f"button:has-text('{text}')"
            
            print(f"Button #{i}:")
            print(f"  Suggested locator: {suggested_locator}")
            print(f"  Text: '{text}'")
            print(f"  Attributes: {attrs}\n")
            
            results.append({
                "type": "button",
                "index": i,
                "attributes": attrs,
                "suggested_locator": suggested_locator
            })
        
        return results
    
    def inspect_links(self) -> list:
        """Find and analyze all link elements."""
        print("🔍 Inspecting link elements...\n")
        links = self.page.locator("a").all()
        results = []
        
        for i, link in enumerate(links, 1):
            attrs = self.get_element_attributes(link)
            text = link.text_content().strip()
            href = link.get_attribute("href")
            attrs["text"] = text
            attrs["href"] = href
            
            suggested_locator = self.suggest_locator(attrs)
            if suggested_locator.startswith("❌") and text:
                suggested_locator = f"a:has-text('{text}')"
            
            print(f"Link #{i}:")
            print(f"  Suggested locator: {suggested_locator}")
            print(f"  Text: '{text}'")
            print(f"  Href: {href}")
            print(f"  Attributes: {attrs}\n")
            
            results.append({
                "type": "link",
                "index": i,
                "attributes": attrs,
                "suggested_locator": suggested_locator
            })
        
        return results
    
    def inspect_selector(self, selector: str) -> list:
        """Inspect elements matching a specific selector."""
        print(f"🔍 Inspecting elements matching: {selector}\n")
        elements = self.page.locator(selector).all()
        results = []
        
        if not elements:
            print(f"❌ No elements found matching selector: {selector}\n")
            return results
        
        print(f"Found {len(elements)} element(s)\n")
        
        for i, elem in enumerate(elements, 1):
            attrs = self.get_element_attributes(elem)
            tag_name = elem.evaluate("el => el.tagName.toLowerCase()")
            text = elem.text_content().strip()
            suggested_locator = self.suggest_locator(attrs)
            
            print(f"Element #{i} ({tag_name}):")
            print(f"  Suggested locator: {suggested_locator}")
            if text:
                print(f"  Text: '{text[:50]}'")
            print(f"  Attributes: {attrs}\n")
            
            results.append({
                "type": tag_name,
                "index": i,
                "attributes": attrs,
                "suggested_locator": suggested_locator,
                "text": text
            })
        
        return results
    
    def generate_page_object_template(self, results: dict) -> str:
        """Generate a Page Object class template with found locators."""
        template = '''from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class NewPage(BasePage):
    """Page object for [PAGE NAME]."""

    # Locators - Generated by PageInspector
'''
        
        # Add inputs
        if results.get("inputs"):
            template += "    # Input fields\n"
            for inp in results["inputs"]:
                inp_name = inp["attributes"].get("name") or ""
                inp_id = inp["attributes"].get("id") or ""
                name = inp_name.upper() or \
                       inp_id.upper() or \
                       f"INPUT_{inp['index']}"
                template += f"    {name} = \"{inp['suggested_locator']}\"\n"
            template += "\n"
        
        # Add buttons
        if results.get("buttons"):
            template += "    # Buttons\n"
            for btn in results["buttons"]:
                btn_id = btn["attributes"].get("id") or ""
                btn_name = btn["attributes"].get("name") or ""
                btn_text = btn["attributes"].get("text") or ""
                name = btn_id.upper() or \
                       btn_name.upper() or \
                       btn_text.upper().replace(" ", "_") or \
                       f"BUTTON_{btn['index']}"
                template += f"    {name} = \"{btn['suggested_locator']}\"\n"
            template += "\n"
        
        # Add links
        if results.get("links"):
            template += "    # Links\n"
            for link in results["links"]:
                link_id = link["attributes"].get("id") or ""
                link_text = link["attributes"].get("text") or ""
                name = link_id.upper() or \
                       link_text[:20].upper().replace(" ", "_") or \
                       f"LINK_{link['index']}"
                template += f"    {name} = \"{link['suggested_locator']}\"\n"
            template += "\n"
        
        template += '''
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Add your methods here
'''
        
        return template
    
    def inspect_all(self, save_template: bool = False) -> dict:
        """Perform a full inspection of the page."""
        print("=" * 80)
        print("🔍 PAGE INSPECTOR")
        print("=" * 80)
        print()
        
        # Take screenshot and save HTML
        self.take_screenshot()
        self.save_html()
        print()
        
        # Inspect all element types
        results = {
            "inputs": self.inspect_inputs(),
            "buttons": self.inspect_buttons(),
            "links": self.inspect_links()
        }
        
        # Generate Page Object template
        if save_template:
            template = self.generate_page_object_template(results)
            filename = "generated_page_object.py"
            with open(filename, "w") as f:
                f.write(template)
            print(f"📝 Page Object template saved: {filename}\n")
        
        return results
    
    def stop(self):
        """Close the browser."""
        if self.browser:
            self.browser.close()
            print("✅ Browser closed")


def main():
    parser = argparse.ArgumentParser(
        description="Inspect web pages and find optimal locators"
    )
    parser.add_argument(
        "--url",
        help="Full URL to inspect (e.g., https://example.com/login)"
    )
    parser.add_argument(
        "--path",
        help=f"Path relative to BASE_URL ({settings.BASE_URL})"
    )
    parser.add_argument(
        "--selector",
        help="Specific CSS selector to inspect (optional)"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode"
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="Generate Page Object template"
    )
    parser.add_argument(
        "--keep-open",
        type=int,
        default=0,
        help="Keep browser open for N seconds (default: 0)"
    )
    
    args = parser.parse_args()
    
    # Determine URL
    if args.url:
        url = args.url
    elif args.path:
        url = f"{settings.BASE_URL.rstrip('/')}{args.path}"
    else:
        print("❌ Error: Either --url or --path is required")
        parser.print_help()
        sys.exit(1)
    
    # Start inspection
    inspector = PageInspector(url, headless=args.headless)
    
    try:
        inspector.start()
        
        if args.selector:
            # Inspect specific selector
            inspector.inspect_selector(args.selector)
        else:
            # Full inspection
            inspector.inspect_all(save_template=args.template)
        
        # Keep browser open if requested
        if args.keep_open > 0 and not args.headless:
            print(f"⏳ Keeping browser open for {args.keep_open} seconds...")
            inspector.page.wait_for_timeout(args.keep_open * 1000)
    
    finally:
        inspector.stop()


if __name__ == "__main__":
    main()
