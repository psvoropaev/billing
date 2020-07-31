from uuid import uuid4

from sqlalchemy import select

from web import models, errors
from web.app.pg import dbpool, transaction
from web.api.v1.serializers import UserWallet



@dbpool
async def get_users(db_pool):
    users_query = select([
        models.user.c.name,
        models.user.c.pasport_data,
        models.wallet.c.bill_number
    ]).select_from(models.wallet.join(models.user))

    async with db_pool.acquire() as conn:
        users = await conn.fetch(users_query)
        return [UserWallet(**dict(user)) for user in users]


def add_user(name: str, pasport_data: str):
    return models.user.insert().values({'name': name, 'pasport_data': pasport_data})


def add_wallet(user_id: int):
    return models.wallet.insert().values({'bill_number': str(uuid4()), 'user_id': user_id})


async def check_user_exist(pasport_data, connection):
    user_query = (
        select([models.user.c.id]).
            select_from(models.user).
            where(models.user.c.pasport_data == pasport_data)
    )
    row = await connection.fetchrow(user_query)
    return bool(row)


@transaction
async def create_user(name: str, pasport_data: str, connection):
    if not await check_user_exist(pasport_data, connection):
        user = await connection.fetchrow(add_user(name, pasport_data))
        user_id = user['id']
        await connection.fetchrow(add_wallet(user_id))
        return user_id
    else:
        raise errors.DuplicateUser(
            f'User with this data already exists, name="{name}", pasport_data="{pasport_data}"'
        )
