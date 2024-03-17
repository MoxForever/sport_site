from fastapi import FastAPI
from fastapi.middleware import Middleware

from middlewares.admin_access import DatabaseMiddleware

from .cities import cities_router
from .requests import requests_router
from .tournaments import tournaments_route


admin_app = FastAPI(
    middleware=[
        Middleware(
            DatabaseMiddleware,
        )
    ],
    redoc_url=None,
    openapi_url=None,
    docs_url=None,
)

admin_app.include_router(cities_router)
admin_app.include_router(requests_router)
admin_app.include_router(tournaments_route)
