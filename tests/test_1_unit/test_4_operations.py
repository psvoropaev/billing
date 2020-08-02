from uuid import uuid4
import pytest
from sqlalchemy import select

import billing.api
from billing import models, errors
from billing.api.v1.controllers import wallets, operations


@pytest.mark.parametrize('amount,balance', [(10, 10), (-10, 0), (0, 0), (13.47, 13.47), (-13.47, 0)])
async def test_refresh_balance(db_conn, amount, balance):
    wallets_db = await db_conn.fetch(select([models.wallet]))
    for wallet_db in wallets_db:
        wallet_db = dict(wallet_db)

        await billing.api.v1.controllers.wallets.refresh_wallet_balance(wallet_db['id'], amount, db_conn)
        current_balance = await wallets.get_wallet_field(wallet_db['bill_number'], 'balance', db_conn)
        assert current_balance == balance


async def test_check_possibility_payment(db_conn):
    wallets_db = [dict(wallet_db) for wallet_db in await db_conn.fetch(select([models.wallet]))][:2]

    wallet_id_recipient = wallets_db[0]['id']
    wallet_id_sender = wallets_db[1]['id']

    reason_db_list = await db_conn.fetch(select([models.reason]))
    for reason_db in reason_db_list:
        reason_db = dict(reason_db)

        correlation_id = str(reason_db['id'])

        is_possibility_payment = await operations.check_possibility_payment(correlation_id, db_conn)
        assert is_possibility_payment

        operation_data = {
            'correlation_id': correlation_id,
            'amount': 0.0,
            'reason_id': reason_db['id']
        }

        if reason_db['using_second_bill_number']:
            await db_conn.fetchrow(
                operations.add_wallet_operation(
                    **dict(
                        wallet_id_sender=wallet_id_sender,
                        wallet_id_recipient=wallet_id_recipient,
                        **operation_data
                    )
                )
            )
            await db_conn.fetchrow(
                operations.add_wallet_operation(
                    **dict(
                        wallet_id_recipient=wallet_id_sender,
                        wallet_id_sender=wallet_id_recipient,
                        **operation_data
                    )
                )
            )
        else:
            await db_conn.fetchrow(
                operations.add_wallet_operation(
                    **dict(
                        wallet_id_recipient=wallet_id_recipient,
                        **operation_data
                    )
                )
            )

        is_possibility_payment = await operations.check_possibility_payment(correlation_id, db_conn)
        assert is_possibility_payment == False


@pytest.mark.parametrize('amount', [0, 1.5, 10, -1.5, -10])
async def test_payment(db_conn, amount):
    wallets_db = [dict(wallet_db) for wallet_db in await db_conn.fetch(select([models.wallet]))][:2]

    bill_num_recipient = wallets_db[0]['bill_number']
    bill_num_sender = wallets_db[1]['bill_number']

    reason_db_list = await db_conn.fetch(select([models.reason]))
    for reason_db in reason_db_list:
        reason_db = dict(reason_db)

        balance_recipient_before = await wallets.get_wallet_field(bill_num_recipient, 'balance', db_conn)
        balance_sender_before = await wallets.get_wallet_field(bill_num_recipient, 'balance', db_conn)

        await operations.payment(
            connection=db_conn,
            correlation_id=str(uuid4()),
            amount=amount,
            reason_code=reason_db['code'],
            bill_num_sender=bill_num_sender if reason_db['using_second_bill_number'] else None,
            bill_num_recipient=bill_num_recipient
        )

        balance_recipient_after = await wallets.get_wallet_field(bill_num_recipient, 'balance', db_conn)
        balance_sender_after = await wallets.get_wallet_field(bill_num_recipient, 'balance', db_conn)

        assert balance_recipient_before + amount == balance_recipient_after
        if reason_db['using_second_bill_number']:
            assert balance_sender_before + amount == balance_sender_after


@pytest.mark.parametrize('correlation_id,error', [
    ('1', errors.OperationAlreadyExists),
    ('-1', errors.NotEnoughFunds)
])
async def test_payment_procces(db_conn, correlation_id, error):
    wallets = await db_conn.fetch(select([models.wallet]))
    bill_number = dict(wallets[0])['bill_number']
    bill_number_sender = dict(wallets[1])['bill_number']
    with pytest.raises(error) as ex:
        await operations.payment_procces(
            connection=db_conn,
            correlation_id=correlation_id,
            amount=9999999,
            reason_code='TRANSFER',
            bill_number_sender=bill_number_sender,
            bill_number=bill_number
        )
