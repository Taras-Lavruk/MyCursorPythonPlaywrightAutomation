"""
Sample API tests using Playwright's built-in request context.

Requires API_BASE_URL (and optionally API_BEARER_TOKEN) to be set in .env.
Tests are skipped automatically when API_BASE_URL is not configured so CI
never silently hits an unrelated third-party host.
"""

from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from config.settings import settings


@pytest.fixture(scope="module")
def api(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    """Module-scoped API request context.

    Skips the entire module when API_BASE_URL is not configured in .env.
    """
    if not settings.API_BASE_URL:
        pytest.skip("API_BASE_URL not configured in .env — skipping API tests")

    headers: dict[str, str] = {}
    if settings.API_BEARER_TOKEN:
        headers["Authorization"] = f"Bearer {settings.API_BEARER_TOKEN}"

    ctx = playwright.request.new_context(
        base_url=settings.API_BASE_URL,
        extra_http_headers=headers,
    )
    yield ctx
    ctx.dispose()


@pytest.mark.api
@pytest.mark.smoke
class TestPostsAPI:
    def test_get_posts_returns_200(self, api: APIRequestContext) -> None:
        """GET /posts should return HTTP 200."""
        response = api.get("/posts")
        assert response.status == 200
