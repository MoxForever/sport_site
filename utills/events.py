import datetime
import uuid
import aio_pika
from fastapi import Request
from pydantic import BaseModel

from models.api import MatchFullAPI, TeamFullAPI, TournamentAPI
from models.db import MatchDB, TournamentDB
from models.db_to_api import (
    match_full_to_model,
    team_full_to_model,
    tournament_to_model,
)


class TournamentUpdate(BaseModel):
    tournament: TournamentAPI
    matches: list[MatchFullAPI]
    teams: list[TeamFullAPI]


async def get_data():
    tournament = await TournamentDB.filter(
        end_date__gt=datetime.datetime.now(tz=datetime.timezone.utc)
    ).first()
    if tournament is None:
        return

    matches = await MatchDB.filter(tournament=tournament).prefetch_related(
        "team_1", "team_2", "judge", "tournament"
    )
    teams = set()
    for i in matches:
        await i.team_1.fetch_related("user_1", "user_2", "tournament")
        await i.team_2.fetch_related("user_1", "user_2", "tournament")
        teams.add(i.team_1)
        teams.add(i.team_2)

    matches = list(sorted(matches, key=lambda i: i.start))

    return TournamentUpdate(
        tournament=tournament_to_model(tournament),
        matches=list(map(match_full_to_model, matches)),
        teams=list(map(team_full_to_model, teams)),
    ).model_dump_json()


async def send_event(connection: aio_pika.Connection):
    channel = await connection.channel()

    exchange = await channel.declare_exchange("event", "fanout")
    await exchange.publish(
        aio_pika.Message(body=(await get_data()).encode("utf-8")), routing_key=""
    )


async def event_subscribe(request: Request):
    channel = await request.state.ampq.channel()
    queue = await channel.declare_queue(uuid.uuid4().hex)
    exchange = await channel.declare_exchange("event", "fanout")
    await queue.bind(exchange, "")

    yield await get_data()

    async for message in queue:
        async with message.process():
            yield message.body.decode()
            if await request.is_disconnected():
                await channel.close()
                return
