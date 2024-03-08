from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise

from models.api import Settings
from endpoints import api_route
from http_site import http_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(db_url=Settings().DB_URL, modules={"models": ["models"]})
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_route)
app.include_router(http_route)
