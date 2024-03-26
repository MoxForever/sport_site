from fastapi import Request
from sse_starlette import EventSourceResponse

from utills.events import event_subscribe



async def tournaments_data(request: Request):
    return EventSourceResponse(event_subscribe(request))
