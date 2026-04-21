import os
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright
from config.settings import settings

# ---------------------------------------------------------------------------
# Browser / context / page fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "headless": settings.HEADLESS,
        "slow_mo": settings.SLOW_MO,
        "args": ["--no-sandbox", "--disable-dev-shm-usage"],
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "viewport": {
            "width": settings.VIEWPORT_WIDTH,
            "height": settings.VIEWPORT_HEIGHT,
        },
        "ignore_https_errors": True,
        "record_video_dir": "reports/videos",
        "record_video_size": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="function")
def context(browser: Browser, browser_context_args: dict, request) -> BrowserContext:
    ctx = browser.new_context(**browser_context_args)
    ctx.set_default_timeout(settings.DEFAULT_TIMEOUT)
    yield ctx
    
    # Only save video if test failed
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        video = ctx.pages[0].video if ctx.pages else None
        if video:
            video_path = video.path()
            print(f"\n📹 Video saved for failed test: {video_path}")
    else:
        # Delete video if test passed
        for page in ctx.pages:
            if page.video:
                try:
                    video_path = page.video.path()
                    ctx.close()
                    if os.path.exists(video_path):
                        os.remove(video_path)
                except Exception:
                    pass
                return
    
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    p = context.new_page()
    yield p
    p.close()


# ---------------------------------------------------------------------------
# API request context fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright):
    ctx = playwright.request.new_context(base_url=settings.API_BASE_URL)
    yield ctx
    ctx.dispose()


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Store test result in the item for context fixture to access
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        page: Page | None = item.funcargs.get("page")
        if page:
            os.makedirs("reports/screenshots", exist_ok=True)
            screenshot_name = item.nodeid.replace("/", "_").replace("::", "_")
            page.screenshot(path=f"reports/screenshots/{screenshot_name}.png", full_page=True)
