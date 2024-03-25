import os
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from utills.listdir_recursively import listdir


http_route = APIRouter()
templates = Jinja2Templates(directory="templates")


def handler_constuctor(path: str):
    async def handler(request: Request):
        return templates.TemplateResponse(request, path)

    return handler


for i in listdir("templates"):
    path = os.path.sep.join(i.split(os.path.sep)[1:])
    route = path.replace(".html", "")
    if route.split(os.path.sep)[-1] == "index":
        route = os.path.sep.join(route.split(os.path.sep)[:-1])
    if not route.startswith("/"):
        route = "/" + route

    http_route.add_route(route, handler_constuctor(path))
