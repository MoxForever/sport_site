import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.db import MatchDB, UserDB
from models.api import UserType
from models.db_to_api import match_to_model, user_to_model

matches_route = APIRouter(prefix="/matches")


class EditMatch(BaseModel):
    id: int
    start: datetime.datetime | None
    judge_id: int | None


@matches_route.get("/list")
async def list_mathes(tournament_id: int):
    return list(
        map(
            match_to_model,
            await MatchDB.filter(tournament_id=tournament_id).prefetch_related(
                "team_1", "team_2"
            ),
        )
    )


@matches_route.get("/judges")
async def list_judges():
    return list(
        map(
            user_to_model, await UserDB.filter(user_type=UserType.JUDGE, confirmed=True)
        )
    )


@matches_route.post("/edit")
async def edit_match(data: EditMatch):
    match = await MatchDB.get_or_none(id=data.id).prefetch_related("team_1", "team_2")
    if match is None:
        raise HTTPException(status_code=400, detail="Такого матча не существует")

    match.judge_id = data.judge_id
    match.start = data.start
    await match.save()
    return match_to_model(match)
