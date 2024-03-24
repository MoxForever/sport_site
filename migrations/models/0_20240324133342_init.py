from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "tournaments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "fio" VARCHAR(256) NOT NULL,
    "email" VARCHAR(320) NOT NULL UNIQUE,
    "user_type" VARCHAR(7) NOT NULL,
    "confirmed" BOOL NOT NULL  DEFAULT False,
    "password_hashed" VARCHAR(256)
);
COMMENT ON COLUMN "users"."user_type" IS 'ATHLETE: ATHLETE\nJUDGE: JUDGE\nADMIN: ADMIN';
CREATE TABLE IF NOT EXISTS "teams" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "tournament_id" INT NOT NULL REFERENCES "tournaments" ("id") ON DELETE CASCADE,
    "user_1_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "user_2_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "match" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "score_1" INT NOT NULL  DEFAULT 0,
    "score_2" INT NOT NULL  DEFAULT 0,
    "start" TIMESTAMPTZ,
    "end" TIMESTAMPTZ,
    "judge_id" INT REFERENCES "users" ("id") ON DELETE CASCADE,
    "team_1_id" INT NOT NULL REFERENCES "teams" ("id") ON DELETE CASCADE,
    "team_2_id" INT NOT NULL REFERENCES "teams" ("id") ON DELETE CASCADE,
    "tournament_id" INT NOT NULL REFERENCES "tournaments" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
