from fastapi import APIRouter, Response

from models.db import CityDB
from models.api import CityAPI
from models.db_to_api import city_to_model

data_route = APIRouter(prefix="/data")


@data_route.get("/cities")
async def cities(response: Response) -> list[CityAPI]:
    return list(map(city_to_model, await CityDB.all()))
