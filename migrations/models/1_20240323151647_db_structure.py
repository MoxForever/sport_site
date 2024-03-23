from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "match" ADD "team_1_id" INT NOT NULL;
        ALTER TABLE "match" ADD "start" TIMESTAMPTZ;
        ALTER TABLE "match" ADD "team_2_id" INT NOT NULL;
        ALTER TABLE "match" ALTER COLUMN "judge_id" DROP NOT NULL;
        ALTER TABLE "match" ADD CONSTRAINT "fk_match_teams_598153e2" FOREIGN KEY ("team_1_id") REFERENCES "teams" ("id") ON DELETE CASCADE;
        ALTER TABLE "match" ADD CONSTRAINT "fk_match_teams_ba524580" FOREIGN KEY ("team_2_id") REFERENCES "teams" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "match" DROP CONSTRAINT "fk_match_teams_ba524580";
        ALTER TABLE "match" DROP CONSTRAINT "fk_match_teams_598153e2";
        ALTER TABLE "match" DROP COLUMN "team_1_id";
        ALTER TABLE "match" DROP COLUMN "start";
        ALTER TABLE "match" DROP COLUMN "team_2_id";
        ALTER TABLE "match" ALTER COLUMN "judge_id" SET NOT NULL;"""
