import hashlib
from tortoise.models import Model
from tortoise import fields

from models.api import UserType


class UserDB(Model):
    id = fields.IntField(pk=True, null=False)
    fio = fields.CharField(256, null=False)
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
    name = fields.CharField(128, null=False)
    start_date = fields.DateField(null=False)
    end_date = fields.DateField(null=False)

    class Meta:
        table = "tournaments"


class TeamDB(Model):
    id = fields.IntField(pk=True, null=False)
    user_1 = fields.ForeignKeyField("models.UserDB", null=False, related_name=False)
    user_2 = fields.ForeignKeyField("models.UserDB", null=False, related_name=False)
    tournament = fields.ForeignKeyField("models.TournamentDB", null=False)

    class Meta:
        table = "teams"


class MatchDB(Model):
    id = fields.IntField(pk=True, null=False)
    score_1 = fields.IntField(null=False, default=0)
    score_2 = fields.IntField(null=False, default=0)
    team_1 = fields.ForeignKeyField("models.TeamDB", null=False, related_name=False)
    team_2 = fields.ForeignKeyField("models.TeamDB", null=False, related_name=False)
    tournament = fields.ForeignKeyField("models.TournamentDB", null=False)
    judge = fields.ForeignKeyField("models.UserDB", null=True)
    start = fields.DatetimeField(null=True)
    end = fields.DatetimeField(null=True)

    class Meta:
        table = "match"
