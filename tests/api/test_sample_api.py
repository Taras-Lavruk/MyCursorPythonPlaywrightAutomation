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
    ctx = playwright.request.new_context(base_url=base_url)
    yield ctx
    ctx.dispose()


@pytest.mark.api
@pytest.mark.smoke
class TestPostsAPI:
    def test_get_posts_returns_200(self, api: APIRequestContext) -> None:
        response = api.get("/posts")
        assert response.status == 200

    def test_get_posts_returns_list(self, api: APIRequestContext) -> None:
        response = api.get("/posts")
        body = response.json()
        assert isinstance(body, list)
        assert len(body) > 0

    def test_get_single_post(self, api: APIRequestContext) -> None:
        response = api.get("/posts/1")
        assert response.status == 200
        post = response.json()
        assert post["id"] == 1
        assert "title" in post
        assert "body" in post

    def test_create_post(self, api: APIRequestContext) -> None:
        payload = {"title": "foo", "body": "bar", "userId": 1}
        response = api.post("/posts", data=str(payload).replace("'", '"'))
        assert response.status == 201

    def test_get_nonexistent_post_returns_404(self, api: APIRequestContext) -> None:
        response = api.get("/posts/99999")
        assert response.status == 404
