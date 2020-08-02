import pytest
from sqlalchemy import select

from billing import models, errors
from billing.api.v1.controllers import reasons, currency


async def test_get_reasons_data(db_conn):
    reason_db_list = await db_conn.fetch(select([models.reason]))
    assert len(reason_db_list) == 2

    for reason_db in reason_db_list:
        reason_db = dict(reason_db)
        reason_id, using_second_bill_number = await reasons.get_reason_data(reason_db['code'], db_conn)

        assert reason_id == reason_db['id']
        assert using_second_bill_number == reason_db['using_second_bill_number']


@pytest.mark.parametrize('code', ['111111', None])
async def test_not_found_reasons(db_conn, code):
    with pytest.raises(errors.NotFound) as ex:
        await reasons.get_reason_data(code, db_conn)


async def test_get_currency_id(db_conn):
    currency_db_list = await db_conn.fetch(select([models.currency]))
    assert len(currency_db_list) == 1

    for currency_db in currency_db_list:
        currency_db = dict(currency_db)
        currency_id = await currency.get_currency_id(currency_db['alias'], db_conn)

        assert currency_id == currency_db['id']


@pytest.mark.parametrize('code', ['111111', None])
async def test_not_found_currency(db_conn, code):
    with pytest.raises(errors.NotFound) as ex:
        await currency.get_currency_id(code, db_conn)
