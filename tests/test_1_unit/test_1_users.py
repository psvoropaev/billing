import pytest

from sqlalchemy import select

from billing import models, errors
from billing.api.v1.controllers import users
from tests.data import users_data


@pytest.mark.parametrize(
    'name,pasport_data',
    users_data
)
async def test_create_users(db_conn, name, pasport_data):
    user_id = await users.create_user(name=name, pasport_data=pasport_data, currency_code='USD', connection=db_conn)
    user_db = await db_conn.fetchrow(select([models.user]).where(models.user.c.id == user_id))
    wallets_db = await db_conn.fetch(select([models.wallet]).where(models.wallet.c.user_id == user_id))

    assert user_db is not None
    assert name == user_db['name']
    assert pasport_data == user_db['pasport_data']
    assert len(wallets_db) == 1
    assert wallets_db[0]['balance'] == 0.0


async def test_get_users(db_conn):
    users_db = await users.get_users(db_conn)
    assert len(users_data) == len(users_db)


@pytest.mark.parametrize(
    'name,pasport_data',
    users_data
)
async def test_duplicate_user_error(db_conn, name, pasport_data):
    with pytest.raises(errors.DuplicateUser) as ex:
        await users.create_user(name=name, pasport_data=pasport_data, currency_code='USD', connection=db_conn)
