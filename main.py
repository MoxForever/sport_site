from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise

from endpoints import api_app
from http_site import http_route
from utills.tortoise_config import TORTOISE_ORM


@asynccontextmanager
async def lifespan(_: FastAPI):
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan, redoc_url=None, openapi_url=None, docs_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/api", api_app)
app.include_router(http_route)
