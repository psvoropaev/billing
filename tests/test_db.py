import pytest

from sqlalchemy import select, func
from asyncpg import UniqueViolationError

from billing.models import user, wallet, operation, reason, currency
from billing.api.v1.controllers import users, wallet, operations, reason



@pytest.mark.parametrize(
    'name,pasport_data,count',
    [
        ('1', '1'),
        ('2', '2'),
        ('3', '3')
    ]
)
async def test_create_users(db_conn, name, pasport_data, count):
    ins = await db_conn.fetchrow(users.add_user(name=name, pasport_data=pasport_data))
    user_id = ins['id']
    user_obj = await db_conn.fetchrow(select([user]).where(user.c.id == user_id))
    assert user_obj is not None
    assert name == user_obj['name']
    assert pasport_data == user_obj['pasport_data']

