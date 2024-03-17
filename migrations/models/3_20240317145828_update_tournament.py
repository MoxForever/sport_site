from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tournaments" ALTER COLUMN "end_date" TYPE DATE USING "end_date"::DATE;
        ALTER TABLE "tournaments" ALTER COLUMN "start_date" TYPE DATE USING "start_date"::DATE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tournaments" ALTER COLUMN "end_date" TYPE TIMESTAMPTZ USING "end_date"::TIMESTAMPTZ;
        ALTER TABLE "tournaments" ALTER COLUMN "start_date" TYPE TIMESTAMPTZ USING "start_date"::TIMESTAMPTZ;"""
