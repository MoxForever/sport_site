import datetime
from enum import Enum
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    SECRET_TOKEN: str


class UserType(Enum):
    ATHLETE = "ATHLETE"
    JUDGE = "JUDGE"
    ADMIN = "ADMIN"


class UserAPI(BaseModel):
    id: int
    fio: str
    email: str
    user_type: UserType
    confirmed: bool


class TournamentAPI(BaseModel):
    id: int
    name: str
    start_date: datetime.date
    end_date: datetime.date


class TeamAPI(BaseModel):
    id: int
    user_1_id: int
    user_2_id: int
    tournament_id: int


class MatchAPI(BaseModel):
    id: int
    judge_id: int | None
    start: datetime.datetime | None
    team_1: TeamAPI
    team_2: TeamAPI
    tournament_id: int
