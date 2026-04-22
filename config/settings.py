import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_URL: str = os.getenv("BASE_URL", "https://rc-manual.jiraalign.xyz/")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://rc-manual.jiraalign.xyz/rest/align/api/2")
    API_BEARER_TOKEN: str = os.getenv("API_BEARER_TOKEN", "")

    TEST_USERNAME: str = os.getenv("TEST_USERNAME", "")
    TEST_PASSWORD: str = os.getenv("TEST_PASSWORD", "")

    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))
    BROWSER: str = os.getenv("BROWSER", "chromium")

    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
    NAVIGATION_TIMEOUT: int = int(os.getenv("NAVIGATION_TIMEOUT", "60000"))

    VIEWPORT_WIDTH: int = 1280
    VIEWPORT_HEIGHT: int = 720


settings = Settings()
