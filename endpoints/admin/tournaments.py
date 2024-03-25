import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.db import MatchDB, TournamentDB
from models.db_to_api import match_to_model, tournament_to_model

tournaments_route = APIRouter(prefix="/tournaments")


class CreateTournamentData(BaseModel):
    name: str
    start_date: datetime.date
    end_date: datetime.date


@tournaments_route.post("/create")
async def create_tournament(data: CreateTournamentData):
    return tournament_to_model(
        await TournamentDB.create(
            name=data.name,
            start_date=data.start_date,
            end_date=data.end_date,
        )
    )


@tournaments_route.get("/list")
async def list_tournaments():
    return list(map(tournament_to_model, await TournamentDB.all()))


@tournaments_route.get("/get")
async def get_tournament(id: int):
    tournament = await TournamentDB.get_or_none(id=id)
    if tournament is None:
        raise HTTPException(
            status_code=400, detail=f"Соревнования с id = {id} не существует"
        )
    return tournament_to_model(tournament)


@tournaments_route.get("/matches")
async def get_matches(tournament_id: int):
    return list(map(match_to_model, await MatchDB.filter(tournament_id=tournament_id)))
