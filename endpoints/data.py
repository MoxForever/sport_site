import asyncio
import datetime
import json
from fastapi import Request
from pydantic import BaseModel
from sse_starlette import EventSourceResponse

from models.api import MatchFullAPI, TeamFullAPI, TournamentAPI
from models.db import MatchDB, TournamentDB
from models.db_to_api import (
    match_full_to_model,
    tournament_to_model,
    team_full_to_model,
)


class TournamentUpdate(BaseModel):
    tournament: TournamentAPI
    matches: list[MatchFullAPI]
    teams: list[TeamFullAPI]


async def event_generator(request):
    while not await request.is_disconnected():
        tournament = await TournamentDB.filter(
            end_date__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).first()
        if tournament is None:
            return

        matches = await MatchDB.filter(tournament=tournament).prefetch_related(
            "team_1", "team_2", "judge", "tournament"
        )
        teams = set()
        for i in matches:
            await i.team_1.fetch_related("user_1", "user_2", "tournament")
            await i.team_2.fetch_related("user_1", "user_2", "tournament")
            teams.add(i.team_1)
            teams.add(i.team_2)

        matches = list(sorted(matches, key=lambda i: i.start))

        yield TournamentUpdate(
            tournament=tournament_to_model(tournament),
            matches=list(map(match_full_to_model, matches)),
            teams=list(map(team_full_to_model, teams)),
        ).model_dump_json()

        await asyncio.sleep(5)


async def tournaments_data(request: Request):
    return EventSourceResponse(event_generator(request))
