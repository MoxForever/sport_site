import hashlib
from tortoise.models import Model
from tortoise import fields

from models.api import UserType


class CityDB(Model):
    id = fields.IntField(pk=True, null=False)
    name = fields.CharField(64, null=False)

    class Meta:
        table = "cities"


class UserDB(Model):
    id = fields.IntField(pk=True, null=False)
    fio = fields.CharField(256, null=False)
    city = fields.ForeignKeyField("models.CityDB", null=False)
    email = fields.CharField(max_length=320, null=False, unique=True)
    user_type = fields.CharEnumField(UserType)
    confirmed = fields.BooleanField(null=False, default=False)
    password_hashed = fields.CharField(256, null=True)

    class Meta:
        table = "users"

    def set_password(self, password: str):
        self.password_hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()

    def check_password(self, password: str):
        return (
            self.password_hashed == hashlib.sha256(password.encode("utf-8")).hexdigest()
        )


class TournamentDB(Model):
    id = fields.IntField(pk=True, null=False)
    city = fields.ForeignKeyField("models.CityDB", null=False)

    class Meta:
        table = "tournaments"


class MatchDB(Model):
    id = fields.IntField(pk=True, null=False)
    tournament = fields.ForeignKeyField("models.TournamentDB", null=False)

    class Meta:
        table = "match"
