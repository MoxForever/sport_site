from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

from models.api import UserType
from models.db import UserDB
from utills.cookie import CookieInvalid, get_cookie_data


class RestrictAccess(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        cookies = list(
            filter(
                lambda i: i.strip().startswith("user="),
                request.headers.get("cookie", "").split(";"),
            )
        )
        if len(cookies) != 1:
            user = None
        else:
            try:
                user = get_cookie_data(cookies[0].split("=", 1)[1])
                user = await UserDB.get_or_none(id=user["user_id"])
                if user and user.user_type not in [UserType.ADMIN, UserType.JUDGE]:
                    user = None
            except CookieInvalid:
                user = None

        if user is None:
            return JSONResponse(status_code=403, content={"detail": "Доступ запрещен"})
        else:
            request.state.user = user
            return await call_next(request)
