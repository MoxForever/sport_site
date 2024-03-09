from enum import Enum
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str


class UserType(Enum):
    ATHLETE = "ATHLETE"
    JUDGE = "JUDGE"
    ADMIN = "ADMIN"


class RegisterData(BaseModel):
    fio: str
    email: str
    city_id: int
    password: str | None
    user_type: UserType


class LogInData(BaseModel):
    email: str
    password: str


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
