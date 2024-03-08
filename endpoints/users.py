from fastapi import APIRouter

from models.api import RegisterData

users_route = APIRouter(prefix="/users")


@users_route.post("/register")
async def register(data: RegisterData):
    print(data)
    return {}


@users_route.post("/log_in")
async def log_in(data: RegisterData):
    print(data)
    return {}
