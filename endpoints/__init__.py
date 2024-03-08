from fastapi import APIRouter

from .users import users_route


api_route = APIRouter(prefix="/api")
api_route.include_router(users_route)
