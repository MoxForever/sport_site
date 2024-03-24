from fastapi import FastAPI
from fastapi.middleware import Middleware

from middlewares.restrict_access import RestrictAccess
from models.api import UserType

from .matches import matches_route
from .requests import requests_router
from .tournaments import tournaments_route
from .teams import teams_route


admin_app = FastAPI(
    middleware=[Middleware(RestrictAccess)],
    redoc_url=None,
    openapi_url=None,
    docs_url=None,
)

admin_app.include_router(matches_route)
admin_app.include_router(requests_router)
admin_app.include_router(tournaments_route)
admin_app.include_router(teams_route)
