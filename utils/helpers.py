import re
import time
import random
import string
from faker import Faker

fake = Faker()


def random_string(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    return fake.email()


def random_phone() -> str:
    return fake.phone_number()


def random_name() -> str:
    return fake.name()


def wait_for(seconds: float) -> None:
    time.sleep(seconds)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_numbers(text: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", text)]


def format_url(base: str, path: str) -> str:
    return f"{base.rstrip('/')}/{path.lstrip('/')}"
