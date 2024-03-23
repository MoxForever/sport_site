from models.api import MatchAPI, TeamAPI, TournamentAPI, UserAPI
from models.db import MatchDB, TeamDB, TournamentDB, UserDB


def user_to_model(user: UserDB):
    return UserAPI(
        id=user.id,
        fio=user.fio,
        email=user.email,
        user_type=user.user_type,
        confirmed=user.confirmed,
    )


def tournament_to_model(tournament: TournamentDB):
    return TournamentAPI(
        id=tournament.id,
        name=tournament.name,
        start_date=tournament.start_date,
        end_date=tournament.end_date,
    )


def team_to_model(team: TeamDB):
    return TeamAPI(
        id=team.id,
        user_1_id=team.user_1_id,
        user_2_id=team.user_2_id,
        tournament_id=team.tournament_id,
    )


def match_to_model(match: MatchDB):
    return MatchAPI(
        id=match.id,
        start=match.start,
        team_1=team_to_model(match.team_1),
        team_2=team_to_model(match.team_2),
        tournament_id=match.tournament_id,
        judge_id=match.judge_id,
    )
