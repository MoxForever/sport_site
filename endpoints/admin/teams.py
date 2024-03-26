from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.api import UserType
from models.db import MatchDB, TeamDB, UserDB
from models.db_to_api import team_to_model, user_to_model

teams_route = APIRouter(prefix="/teams")


class CreateTeam(BaseModel):
    user_1_id: int
    user_2_id: int
    tournament_id: int


class UpdateTeam(BaseModel):
    id: int
    user_1_id: int
    user_2_id: int


class DeleteTeam(BaseModel):
    id: int


@teams_route.get("/candidates")
async def list_candidates():
    return list(
        map(
            user_to_model,
            await UserDB.filter(user_type=UserType.ATHLETE, confirmed=True),
        )
    )


@teams_route.post("/create")
async def create_team(data: CreateTeam):
    team = await TeamDB.create(
        user_1_id=data.user_1_id,
        user_2_id=data.user_2_id,
        tournament_id=data.tournament_id,
    )
    for i in await TeamDB.filter(tournament_id=data.tournament_id, id__not=team.id):
        await MatchDB.create(team_1=i, team_2=team, tournament_id=data.tournament_id)
    return team_to_model(team)


@teams_route.get("/list")
async def list_teams(tournament_id: int):
    return list(map(team_to_model, await TeamDB.filter(tournament_id=tournament_id)))


@teams_route.post("/edit")
async def update_team(data: UpdateTeam):
    team = await TeamDB.get_or_none(id=data.id)
    if team is None:
        raise HTTPException(status_code=400, detail="Team does not exists")

    team.user_1_id = data.user_1_id
    team.user_2_id = data.user_2_id
    await team.save()

    return team_to_model(team)


@teams_route.post("/delete")
async def delete_team(data: DeleteTeam):
    team = await TeamDB.get_or_none(id=data.id)
    if team is not None:
        await team.delete()

    return "OK"
