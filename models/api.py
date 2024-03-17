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
    city_id: int
    user_type: UserType
    confirmed: bool


class CityAPI(BaseModel):
    id: int
    name: str


class TournamentAPI(BaseModel):
    id: int
    name: str
    city_id: int
    start_date: datetime.date
    end_date: datetime.date
