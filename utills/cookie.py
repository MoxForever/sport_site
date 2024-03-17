import base64
import hashlib
import json
from typing import Any

from models.api import Settings


class CookieInvalid(Exception):
    pass


def create_cookie(data: dict) -> str:
    first = base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")
    second = hashlib.sha256(
        f"{first}:{Settings().SECRET_TOKEN}".encode("utf-8")
    ).hexdigest()
    return f"{first}:{second}"


def get_cookie_data(cookie: str) -> dict[str, Any]:
    cookie_data = json.loads(base64.b64decode(cookie.split(":")[0].encode("utf-8")))
    valid_cookie = create_cookie(cookie_data)
    if valid_cookie != cookie:
        raise CookieInvalid()

    return cookie_data
