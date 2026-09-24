"""
Root conftest.py — project-level pytest fixtures and hooks.

Fixture hierarchy:
  browser_type_launch_args  (session) — browser launch settings
  browser_context_args      (session) — context defaults (viewport, https, video)
  auth_state                (session) — performs login once; saves storage state
  context                   (function) — fresh BrowserContext per test + trace
  page                      (function) — Page within the function context
  authenticated_context     (function) — context pre-loaded with auth storage state
  authenticated_page        (function) — page within authenticated_context

Key improvements over original:
  - context fixture: video cleanup logic fixed; Playwright traces added on failure
  - auth_state fixture: login runs once per session using storageState
  - No hardcoded waits (wait_for_timeout) — explicit locator waits only
  - print() → logging
  - Video recording is opt-in via RECORD_VIDEO=true env var (off by default)
"""

import contextlib
import logging
import os
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import APIRequestContext, Browser, BrowserContext, Page, Playwright

from config.settings import settings
from utils.helpers import dismiss_popups

_logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Browser / context configuration
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict[str, Any]) -> dict[str, Any]:  # type: ignore[override]
    """Override launch args with project settings."""
    return {
        **browser_type_launch_args,
        "headless": settings.HEADLESS,
        "slow_mo": settings.SLOW_MO,
        "args": ["--no-sandbox", "--disable-dev-shm-usage"],
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict[str, Any]) -> dict[str, Any]:  # type: ignore[override]
    """Override context args with project settings.

    Video recording is only enabled when RECORD_VIDEO=true is set, avoiding
    the disk overhead on every test run by default.
    """
    ctx_args: dict[str, Any] = {
        **browser_context_args,
        "viewport": {
            "width": settings.VIEWPORT_WIDTH,
            "height": settings.VIEWPORT_HEIGHT,
        },
        "ignore_https_errors": True,
    }
    if settings.RECORD_VIDEO:
        os.makedirs("reports/videos", exist_ok=True)
        ctx_args["record_video_dir"] = "reports/videos"
        ctx_args["record_video_size"] = {
            "width": settings.VIEWPORT_WIDTH,
            "height": settings.VIEWPORT_HEIGHT,
        }
        _logger.info("Video recording enabled → reports/videos/")
    return ctx_args


# ---------------------------------------------------------------------------
# Function-scoped context with traces and conditional video cleanup
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def context(
    browser: Browser,
    browser_context_args: dict[str, Any],
    request: pytest.FixtureRequest,
) -> Generator[BrowserContext, None, None]:
    """Function-scoped context with Playwright trace recording.

    On failure  : trace zip is saved to reports/traces/<test_name>.zip
    On success  : trace is discarded; video deleted (if recording was enabled)
    """
    os.makedirs("reports/traces", exist_ok=True)

    ctx = browser.new_context(**browser_context_args)
    ctx.set_default_timeout(settings.DEFAULT_TIMEOUT)
    ctx.tracing.start(screenshots=True, snapshots=True)

    yield ctx

    failed: bool = getattr(getattr(request.node, "rep_call", None), "failed", False)
    safe_name = (
        request.node.nodeid
        .replace("/", "_")
        .replace("::", "_")
        .replace(" ", "_")
    )

    if failed:
        # Persist trace so engineers can open it with `playwright show-trace`
        trace_path = f"reports/traces/{safe_name}.zip"
        ctx.tracing.stop(path=trace_path)
        _logger.warning("Test FAILED — trace saved: %s", trace_path)
        if settings.RECORD_VIDEO:
            for p in ctx.pages:
                if p.video:
                    with contextlib.suppress(Exception):
                        _logger.warning("Video saved: %s", p.video.path())
        ctx.close()
    else:
        ctx.tracing.stop()  # Discard trace — test passed
        # Collect video paths before closing (file is finalised on ctx.close)
        video_paths: list[str] = []
        if settings.RECORD_VIDEO:
            for p in ctx.pages:
                if p.video:
                    with contextlib.suppress(Exception):
                        video_paths.append(p.video.path())
        ctx.close()
        # Remove videos for passing tests to save disk space
        for vp in video_paths:
            with contextlib.suppress(OSError):
                os.remove(vp)


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Standard unauthenticated page fixture."""
    p = context.new_page()
    yield p
    p.close()


# ---------------------------------------------------------------------------
# Session-scoped auth state (login once per session)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def auth_state(
    browser: Browser,
    tmp_path_factory: pytest.TempPathFactory,
) -> Generator[Path, None, None]:
    """Perform login once per test session and persist the browser storage state.

    Each test that uses ``authenticated_page`` receives a fresh context
    pre-loaded with this state — no repeated UI logins.

    Skips automatically if TEST_USERNAME / TEST_PASSWORD are not configured.
    """
    if not settings.has_credentials:
        pytest.skip("auth_state: TEST_USERNAME / TEST_PASSWORD not set in .env")

    auth_file: Path = tmp_path_factory.getbasetemp() / "auth_state.json"

    # Lightweight context — no video, no trace needed for setup
    ctx = browser.new_context(
        viewport={"width": settings.VIEWPORT_WIDTH, "height": settings.VIEWPORT_HEIGHT},
        ignore_https_errors=True,
    )
    try:
        p = ctx.new_page()
        p.set_default_timeout(settings.DEFAULT_TIMEOUT)
        p.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT)

        from pages.login_page import LoginPage  # avoid circular import at module level
        login = LoginPage(p)
        login.open()
        dismiss_popups(p)
        login.login(settings.TEST_USERNAME, settings.TEST_PASSWORD)
        p.wait_for_load_state("networkidle")

        if "login" in p.url.lower():
            pytest.fail(
                "auth_state fixture: login failed — verify TEST_USERNAME / TEST_PASSWORD in .env"
            )

        dismiss_popups(p)
        ctx.storage_state(path=str(auth_file))
        _logger.info("Auth storage state saved: %s", auth_file)
    finally:
        ctx.close()

    yield auth_file
    # auth_file lives in pytest's tmp dir; no explicit cleanup needed


# ---------------------------------------------------------------------------
# Authenticated fixtures (use these in tests that require login)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def authenticated_context(
    browser: Browser,
    browser_context_args: dict[str, Any],
    auth_state: Path,
    request: pytest.FixtureRequest,
) -> Generator[BrowserContext, None, None]:
    """Function-scoped context pre-loaded with authenticated storage state.

    Saves a Playwright trace zip on test failure (mirrors ``context`` fixture).
    """
    os.makedirs("reports/traces", exist_ok=True)

    ctx = browser.new_context(**browser_context_args, storage_state=str(auth_state))
    ctx.set_default_timeout(settings.DEFAULT_TIMEOUT)
    ctx.tracing.start(screenshots=True, snapshots=True)

    yield ctx

    failed: bool = getattr(getattr(request.node, "rep_call", None), "failed", False)
    safe_name = (
        request.node.nodeid
        .replace("/", "_")
        .replace("::", "_")
        .replace(" ", "_")
    )

    if failed:
        trace_path = f"reports/traces/{safe_name}.zip"
        ctx.tracing.stop(path=trace_path)
        _logger.warning("Test FAILED (authenticated) — trace saved: %s", trace_path)
    else:
        ctx.tracing.stop()  # discard — test passed

    ctx.close()


@pytest.fixture(scope="function")
def authenticated_page(
    authenticated_context: BrowserContext,
) -> Generator[Page, None, None]:
    """Function-scoped page with an already-authenticated session.

    Navigates to BASE_URL on creation and dismisses any post-login popups,
    so tests can start interacting with the app immediately.
    """
    p = authenticated_context.new_page()
    p.goto(settings.BASE_URL)
    p.wait_for_load_state("networkidle")
    dismiss_popups(p)
    yield p
    p.close()


# ---------------------------------------------------------------------------
# API request context
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    """Session-scoped Playwright API request context."""
    headers: dict[str, str] = {}
    if settings.API_BEARER_TOKEN:
        headers["Authorization"] = f"Bearer {settings.API_BEARER_TOKEN}"
    ctx = playwright.request.new_context(
        base_url=settings.API_BASE_URL,
        extra_http_headers=headers,
    )
    yield ctx
    ctx.dispose()


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator[None, None, None]:
    """Attach test outcome to the item node so fixtures can inspect it.

    Also captures a full-page screenshot on test failure.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        page: Page | None = item.funcargs.get("page")  # type: ignore[assignment]
        if page:
            os.makedirs("reports/screenshots", exist_ok=True)
            safe_name = (
                item.nodeid
                .replace("/", "_")
                .replace("::", "_")
                .replace(" ", "_")
            )
            screenshot_path = f"reports/screenshots/{safe_name}.png"
            with contextlib.suppress(Exception):
                page.screenshot(path=screenshot_path, full_page=True)
                _logger.warning("Screenshot saved: %s", screenshot_path)
