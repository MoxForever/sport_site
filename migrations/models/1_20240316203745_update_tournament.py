from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tournaments" ADD "start_date" TIMESTAMPTZ NOT NULL;
        ALTER TABLE "tournaments" ADD "end_date" TIMESTAMPTZ NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tournaments" DROP COLUMN "start_date";
        ALTER TABLE "tournaments" DROP COLUMN "end_date";"""
