"""
Sample API tests using Playwright's built-in request context.
These tests hit https://jsonplaceholder.typicode.com as a live demo target.
Replace BASE_URL / API_BASE_URL in your .env with your actual endpoints.
"""
import pytest
from playwright.sync_api import APIRequestContext
from config.settings import settings


@pytest.fixture(scope="module")
def api(playwright):
    base_url = settings.API_BASE_URL or "https://jsonplaceholder.typicode.com"
    headers = {}
    if settings.API_BEARER_TOKEN:
        headers["Authorization"] = f"Bearer {settings.API_BEARER_TOKEN}"
    ctx = playwright.request.new_context(base_url=base_url, extra_http_headers=headers)
    yield ctx
    ctx.dispose()


@pytest.mark.api
@pytest.mark.smoke
class TestPostsAPI:
    def test_get_posts_returns_200(self, api: APIRequestContext) -> None:
        response = api.get("/posts")
        assert response.status == 200
