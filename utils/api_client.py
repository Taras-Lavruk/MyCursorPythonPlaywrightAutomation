import json
from typing import Any
from playwright.sync_api import APIRequestContext
from config.settings import settings


class APIClient:
    """Thin wrapper around Playwright's APIRequestContext for API-level tests."""

    def __init__(self, request: APIRequestContext) -> None:
        self.request = request
        self.base_url = settings.API_BASE_URL

    def get(self, path: str, params: dict | None = None, headers: dict | None = None) -> Any:
        response = self.request.get(
            f"{self.base_url}{path}",
            params=params or {},
            headers=headers or {},
        )
        return response

    def post(self, path: str, data: dict | None = None, headers: dict | None = None) -> Any:
        response = self.request.post(
            f"{self.base_url}{path}",
            data=json.dumps(data or {}),
            headers={"Content-Type": "application/json", **(headers or {})},
        )
        return response

    def put(self, path: str, data: dict | None = None, headers: dict | None = None) -> Any:
        response = self.request.put(
            f"{self.base_url}{path}",
            data=json.dumps(data or {}),
            headers={"Content-Type": "application/json", **(headers or {})},
        )
        return response

    def delete(self, path: str, headers: dict | None = None) -> Any:
        response = self.request.delete(
            f"{self.base_url}{path}",
            headers=headers or {},
        )
        return response
