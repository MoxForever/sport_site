from models.api import CityAPI, UserAPI
from models.db import CityDB, UserDB


def city_to_model(city: CityDB):
    return CityAPI(id=city.id, name=city.name)


def user_to_model(user: UserDB):
    return UserAPI(
        id=user.id,
        fio=user.fio,
        email=user.email,
        city_id=user.city_id,
        user_type=user.user_type,
        confirmed=user.confirmed,
    )
