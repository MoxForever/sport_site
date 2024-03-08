from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


http_route = APIRouter()
templates = Jinja2Templates(directory="static")


@http_route.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse(request, "main.html")


@http_route.get("/log_in")
async def main_page(request: Request):
    return templates.TemplateResponse(request, "log_in.html")


@http_route.get("{path:path}")
async def request_404():
    return RedirectResponse("/")
