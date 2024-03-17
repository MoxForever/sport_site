from models.api import CityAPI, TournamentAPI, UserAPI
from models.db import CityDB, TournamentDB, UserDB


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


def tournament_to_model(tournament: TournamentDB):
    return TournamentAPI(
        id=tournament.id,
        name=tournament.name,
        city_id=tournament.city_id,
        start_date=tournament.start_date,
        end_date=tournament.end_date,
    )
