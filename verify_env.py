#!/usr/bin/env python3
"""
Verification script to check that environment variables are properly loaded.
Run this script to verify your .env configuration before running tests.

Usage:
    python verify_env.py
    # or
    make verify-env
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings


def print_header(text: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_setting(name: str, value: any, is_sensitive: bool = False) -> None:
    """Print a setting with its value."""
    # Handle different value types
    is_set = value is not None and value != ""
    
    if is_sensitive and is_set:
        display_value = "****" + str(value)[-4:] if len(str(value)) > 4 else "****"
    elif not is_set:
        display_value = "❌ NOT SET"
    else:
        display_value = value
    
    status = "✅" if is_set else "❌"
    print(f"{status} {name:25} = {display_value}")


def verify_environment() -> bool:
    """Verify all environment variables are properly configured."""
    print_header("Environment Configuration Verification")
    
    all_valid = True
    
    # Required settings
    print("\n📋 Required Settings:")
    print("-" * 60)
    
    required_settings = [
        ("BASE_URL", settings.BASE_URL, False),
        ("API_BASE_URL", settings.API_BASE_URL, False),
    ]
    
    for name, value, is_sensitive in required_settings:
        print_setting(name, value, is_sensitive)
        if not value:
            all_valid = False
    
    # Credentials (optional but recommended)
    print("\n🔐 Credentials (optional for some tests):")
    print("-" * 60)
    
    credential_settings = [
        ("TEST_USERNAME", settings.TEST_USERNAME, True),
        ("TEST_PASSWORD", settings.TEST_PASSWORD, True),
    ]
    
    for name, value, is_sensitive in credential_settings:
        print_setting(name, value, is_sensitive)
    
    # Browser settings
    print("\n🌐 Browser Settings:")
    print("-" * 60)
    
    browser_settings = [
        ("HEADLESS", settings.HEADLESS, False),
        ("SLOW_MO", settings.SLOW_MO, False),
        ("BROWSER", settings.BROWSER, False),
    ]
    
    for name, value, is_sensitive in browser_settings:
        print_setting(name, value, is_sensitive)
    
    # Timeout settings
    print("\n⏱️  Timeout Settings:")
    print("-" * 60)
    
    timeout_settings = [
        ("DEFAULT_TIMEOUT", settings.DEFAULT_TIMEOUT, False),
        ("NAVIGATION_TIMEOUT", settings.NAVIGATION_TIMEOUT, False),
    ]
    
    for name, value, is_sensitive in timeout_settings:
        print_setting(name, value, is_sensitive)
    
    # Viewport settings
    print("\n📐 Viewport Settings:")
    print("-" * 60)
    
    viewport_settings = [
        ("VIEWPORT_WIDTH", settings.VIEWPORT_WIDTH, False),
        ("VIEWPORT_HEIGHT", settings.VIEWPORT_HEIGHT, False),
    ]
    
    for name, value, is_sensitive in viewport_settings:
        print_setting(name, value, is_sensitive)
    
    # Summary
    print_header("Summary")
    
    if all_valid:
        print("✅ All required settings are configured!")
        print("\nYou can now run tests:")
        print("  • make test")
        print("  • make test-login")
        print("  • pytest tests/e2e/")
    else:
        print("❌ Some required settings are missing!")
        print("\nPlease check your .env file:")
        print("  1. Ensure .env exists: ls -la .env")
        print("  2. Copy from example: cp .env.example .env")
        print("  3. Edit with your values: nano .env")
        print("\nFor more information, see: ENVIRONMENT.md")
    
    print("\n" + "=" * 60 + "\n")
    
    return all_valid


if __name__ == "__main__":
    try:
        is_valid = verify_environment()
        sys.exit(0 if is_valid else 1)
    except Exception as e:
        print(f"\n❌ Error verifying environment: {e}")
        print("\nMake sure:")
        print("  1. You're in the project root directory")
        print("  2. Virtual environment is activated")
        print("  3. Dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
