from uuid import uuid4

from sqlalchemy import select, and_

from web import models
from web.app.pg import dbpool, transaction
from web.app.config import config


@dbpool
async def get_users(db_pool):
    users_query = select([
        models.user.c.name,
        models.wallet.c.code
    ]).select_from(models.user, models.wallet)

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(users_query)
        return rows


def add_user(name: str):
    return models.user.insert().values({'name': name})


def add_wallet(user_id: int):
    wallet_code = uuid4()
    return models.user.insert().values({'code': wallet_code, 'user_id': user_id})


@transaction
async def create_user(name: str, connection):
    user = await connection.fetchrow(add_user(name))
    wallet = await connection.fetchrow(add_wallet(user.c.id))
