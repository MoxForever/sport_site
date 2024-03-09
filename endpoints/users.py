from fastapi import APIRouter, HTTPException
from tortoise.exceptions import IntegrityError

from models.api import LogInData, RegisterData, UserAPI, UserType
from models.db import UserDB
from models.db_to_api import user_to_model

users_route = APIRouter(prefix="/users")


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
async def log_in(data: LogInData) -> UserAPI:
    user = await UserDB.get_or_none(email=data.email)
    if user is None or not user.check_password(data.password):
        raise HTTPException(status_code=404, detail="Проверьте email и пароль!")
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
    return user_to_model(user)
