from sqlalchemy import select

from billing import models, errors
from billing.api.v1.controllers.wallet import add_wallet
from billing.app.pg import dbpool, transaction
from billing.api.v1.serializers import UserWalletSchema


@dbpool
async def get_users(db_pool):
    users_query = select([
        models.user.c.name,
        models.user.c.pasport_data,
        models.wallet.c.bill_number,
        models.wallet.c.balance
    ]).select_from(models.wallet.join(models.user))

    async with db_pool.acquire() as conn:
        users = await conn.fetch(users_query)
        return [UserWalletSchema(**dict(user)) for user in users]


def add_user(name: str, pasport_data: str):
    return models.user.insert().values({'name': name, 'pasport_data': pasport_data})


async def check_user_exist(pasport_data, connection) -> bool:
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
