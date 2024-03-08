from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "cities" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL
);
        CREATE TABLE IF NOT EXISTS "matchdb" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "tournament_id" INT NOT NULL REFERENCES "tournamentdb" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "tournamentdb" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "city_id" INT NOT NULL REFERENCES "cities" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "fio" VARCHAR(256) NOT NULL,
    "user_type" VARCHAR(7) NOT NULL,
    "confirmed" BOOL NOT NULL  DEFAULT False,
    "password_hashed" VARCHAR(256),
    "city_id" INT NOT NULL REFERENCES "cities" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "users"."user_type" IS 'ATHLETE: ATHLETE\nJUDGE: JUDGE\nADMIN: ADMIN';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "cities";
        DROP TABLE IF EXISTS "matchdb";
        DROP TABLE IF EXISTS "tournamentdb";
        DROP TABLE IF EXISTS "users";"""
