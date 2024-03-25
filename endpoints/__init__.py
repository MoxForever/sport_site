from fastapi import FastAPI

from .users import users_route
from .data import tournaments_data
from .admin import admin_app


api_app = FastAPI(prefix="/api", redoc_url=None, openapi_url=None, docs_url=None)
api_app.include_router(users_route)
api_app.get("/data")(tournaments_data)
api_app.mount("/admin", admin_app)
