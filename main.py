from contextlib import asynccontextmanager

import aio_pika
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise

from endpoints import api_app
from http_site import http_route
from models.api import Settings
from utills.tortoise_config import TORTOISE_ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(TORTOISE_ORM)
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    ampq = await aio_pika.connect_robust(Settings().RABBIT_URL)
    print(ampq.transport)

    yield {"ampq": ampq}

    await ampq.close()
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan, redoc_url=None, openapi_url=None, docs_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/api", api_app)
app.include_router(http_route)
