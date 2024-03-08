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
    password: str
    user_type: UserType


class LogInData(BaseModel):
    email: str
    password: str
