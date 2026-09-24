"""
utils — project-wide utility package.

Public API re-exported here so consumers can write::

    from utils import dismiss_popups, random_email, random_string

instead of importing from the sub-module directly.
"""

from utils.helpers import (
    dismiss_popups,
    extract_numbers,
    format_url,
    normalize_whitespace,
    random_email,
    random_name,
    random_phone,
    random_string,
)

__all__ = [
    "dismiss_popups",
    "extract_numbers",
    "format_url",
    "normalize_whitespace",
    "random_email",
    "random_name",
    "random_phone",
    "random_string",
]
