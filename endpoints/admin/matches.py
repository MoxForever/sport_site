import datetime
from typing import Literal
from fastapi import APIRouter, FastAPI, HTTPException, Request
from pydantic import BaseModel

from models.db import MatchDB, UserDB
from models.api import UserType
from models.db_to_api import match_full_to_model, match_to_model, user_to_model
from utills.events import send_event

matches_route = APIRouter(prefix="/matches")


class EditMatch(BaseModel):
    id: int
    start: datetime.datetime | None
    judge_id: int | None


class EndMatch(BaseModel):
    id: int


class ScoreMatch(BaseModel):
    id: int
    team_1: Literal[-1] | Literal[0] | Literal[1]
    team_2: Literal[-1] | Literal[0] | Literal[1]


@matches_route.get("/list")
async def list_mathes(tournament_id: int):
    return list(
        map(
            match_to_model,
            await MatchDB.filter(tournament_id=tournament_id)
            .order_by("start")
            .prefetch_related("team_1", "team_2"),
        )
    )


@matches_route.get("/get")
async def get_match(match_id: int):
    match = await MatchDB.get_or_none(id=match_id).prefetch_related(
        "judge",
        "team_1",
        "team_2",
        "tournament",
    )
    await match.team_1.fetch_related("tournament", "user_1", "user_2")
    await match.team_2.fetch_related("tournament", "user_1", "user_2")
    if match is None:
        raise HTTPException(status_code=400, detail="Матч не существует")

    return match_full_to_model(match)


@matches_route.post("/end")
async def end_match(data: EndMatch, request: Request):
    match = await MatchDB.get(id=data.id)
    match.end = datetime.datetime.now(tz=datetime.timezone.utc)
    await match.save()
    await send_event(request.state.ampq)
    return "OK"


@matches_route.post("/score")
async def add_scores(data: ScoreMatch, request: Request):
    match = await MatchDB.get_or_none(id=data.id)
    match.score_1 += data.team_1
    match.score_2 += data.team_2
    if match.score_1 < 0 or match.score_2 < 0:
        raise HTTPException(status_code=400, detail="Очков не может быть меньше нуля")
    await match.save()
    await send_event(request.state.ampq)

    return "OK"


@matches_route.get("/list_judge")
async def judge_list_match(request: Request):
    return list(
        map(
            match_to_model,
            await MatchDB.filter(
                start__not_isnull=True, end__isnull=True, judge_id=request.state.user.id
            )
            .order_by("start")
            .prefetch_related("team_1", "team_2"),
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
async def edit_match(data: EditMatch, request: Request):
    match = await MatchDB.get_or_none(id=data.id).prefetch_related("team_1", "team_2")
    if match is None:
        raise HTTPException(status_code=400, detail="Такого матча не существует")

    match.judge_id = data.judge_id
    match.start = data.start
    await match.save()
    await send_event(request.state.ampq)
    return match_to_model(match)
