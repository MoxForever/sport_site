from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise

from models.api import Settings
from endpoints.users import users_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(db_url=Settings().DB_URL, modules={"models": ["models"]})
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)
app.include_router(users_route)
