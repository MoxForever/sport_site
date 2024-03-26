import datetime
from enum import Enum
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    SECRET_TOKEN: str
    RABBIT_URL: str

    @property
    def DB_URL(self):
        return f"mysql://root:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


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


class TeamFullAPI(BaseModel):
    id: int
    user_1: UserAPI
    user_2: UserAPI
    tournament: TournamentAPI


class MatchAPI(BaseModel):
    id: int
    judge_id: int | None
    start: datetime.datetime | None
    end: datetime.datetime | None
    team_1: TeamAPI
    team_2: TeamAPI
    score_1: int
    score_2: int
    tournament_id: int


class MatchFullAPI(BaseModel):
    id: int
    judge: UserAPI | None
    start: datetime.datetime | None
    end: datetime.datetime | None
    team_1: TeamFullAPI
    team_2: TeamFullAPI
    score_1: int
    score_2: int
    tournament: TournamentAPI
