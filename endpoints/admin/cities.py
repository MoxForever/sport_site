from typing import Literal
from fastapi import APIRouter
from pydantic import BaseModel

from models.api import CityAPI
from models.db import CityDB
from models.db_to_api import city_to_model


cities_router = APIRouter(prefix="/cities")


class DeleteCity(BaseModel):
    id: int


class CreateCity(BaseModel):
    name: str


@cities_router.post("/delete")
async def delete_city(city: DeleteCity) -> Literal["OK"]:
    await CityDB.get(id=city.id).delete()
    return "OK"


@cities_router.post("/create")
async def create_city(city: CreateCity) -> CityAPI:
    return city_to_model(await CityDB.create(name=city.name))
