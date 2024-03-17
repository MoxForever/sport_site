from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel
from tortoise.exceptions import IntegrityError

from models.api import UserAPI, UserType
from models.db import UserDB
from models.db_to_api import user_to_model
from utills.cookie import CookieInvalid, create_cookie, get_cookie_data

users_route = APIRouter(prefix="/users")


class RegisterData(BaseModel):
    fio: str
    email: str
    city_id: int
    password: str | None
    user_type: UserType


class LogInData(BaseModel):
    email: str
    password: str


@users_route.get("/me")
async def me(request: Request, response: Response) -> UserAPI:
    cookie_data = request.cookies.get("user")
    if cookie_data is None:
        raise HTTPException(status_code=400, detail="Вы не вошли в учетную запись")

    try:
        user_data = get_cookie_data(cookie_data)
    except CookieInvalid:
        response.delete_cookie("user")
        raise HTTPException(status_code=400, detail="Сессия просрочена")

    return user_to_model(await UserDB.get(id=user_data["user_id"]))


@users_route.post("/register")
async def register(data: RegisterData) -> UserAPI:
    if data.password is None != (data.user_type == UserType.ATHLETE):
        raise HTTPException(
            status_code=400, detail="Администратор и судья обязан установить пароль"
        )

    user = UserDB(
        fio=data.fio,
        city_id=data.city_id,
        email=data.email,
        user_type=data.user_type,
    )
    if data.password is not None:
        user.set_password(data.password)

    try:
        await user.save()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Такой email уже зарегестрирован")

    return user_to_model(user)


@users_route.post("/log_in")
async def log_in(data: LogInData, response: Response) -> UserAPI:
    user = await UserDB.get_or_none(email=data.email)
    if user is None or not user.check_password(data.password):
        raise HTTPException(status_code=400, detail="Проверьте email и пароль!")
    if user.user_type == UserType.ATHLETE:
        raise HTTPException(
            status_code=400,
            detail="Участникам соревнования не предоставляется доступ в ЛК",
        )
    if not user.confirmed:
        raise HTTPException(
            status_code=400,
            detail="Ваша учетная запись не подтверждена, свяжитесь с организатором соревнований",
        )

    response.set_cookie("user", create_cookie({"user_id": user.id}), max_age=604800)
    return user_to_model(user)
