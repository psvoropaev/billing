import pytest
from sqlalchemy import select

from billing import models, errors
from billing.api.v1.controllers import wallets


@pytest.mark.parametrize('field', ['id', 'balance', 'user_id'])
async def test_get_wallet_field(db_conn, field):
    wallets_db = await db_conn.fetch(select([models.wallet]))
    for wallet_db in wallets_db:
        wallet_db = dict(wallet_db)
        fileld_value = await wallets.get_wallet_field(wallet_db['bill_number'], field, db_conn)
        assert fileld_value == wallet_db[field]

    with pytest.raises(errors.BadParams) as ex:
        await wallets.get_wallet_field('111', None, db_conn)

    with pytest.raises(errors.NotFound) as ex:
        await wallets.get_wallet_field('111', '111', db_conn)
