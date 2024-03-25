from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.api import UserAPI
from models.db import UserDB
from models.db_to_api import user_to_model


requests_router = APIRouter(prefix="/requests")


class ProcessUser(BaseModel):
    user_id: int
    confirmed: bool


@requests_router.get("/list")
async def list_users() -> list[UserAPI]:
    return list(map(user_to_model, await UserDB.filter(confirmed=False)))


@requests_router.post("/process")
async def process_user(data: ProcessUser) -> Literal["OK"]:
    user = await UserDB.get_or_none(id=data.user_id)
    if user is None:
        raise HTTPException(status_code=400, detail="User does not exists")

    if data.confirmed:
        user.confirmed = True
        await user.save()
    else:
        await user.delete()

    return "OK"
