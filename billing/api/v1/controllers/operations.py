from sqlalchemy import select

from billing import models
from billing.errors import OperationAlreadyExists, NotEnoughFunds
from billing.api.v1.controllers.reasons import get_reason_data
from billing.api.v1.controllers.wallets import get_wallet_field, refresh_wallet_balance
from billing.app.pg import transaction


def add_wallet_operation(correlation_id: str, amount: float, reason_id: int, wallet_id_recipient: int,
                         wallet_id_sender: int = None):
    return models.operation.insert().values({
        'correlation_id': correlation_id,
        'amount': amount,
        'reason_id': reason_id,
        'wallet_id': wallet_id_recipient,
        'connected_wallet_id': wallet_id_sender
    })


async def check_possibility_payment(correlation_id: str, connection) -> bool:
    operation_query = (
        select([models.operation.c.id]).
            select_from(models.operation).
            where(models.operation.c.correlation_id == correlation_id)
    )
    row = await connection.fetch(operation_query)
    return not bool(row)


async def payment(connection, correlation_id: str, amount: float, reason_code: str, bill_num_recipient: str,
                  bill_num_sender: str = None):
    reason_id, using_second_bill_number = await get_reason_data(reason_code, connection)
    wallet_id_recipient = await get_wallet_field(bill_num_recipient, 'id', connection)
    wallet_id_sender = await get_wallet_field(bill_num_sender, 'id', connection) if using_second_bill_number else None

    # зачислить средста на счет
    await connection.fetchrow(
        add_wallet_operation(
            correlation_id,
            amount,
            reason_id,
            wallet_id_recipient,
            wallet_id_sender
        )
    )
    await refresh_wallet_balance(wallet_id_recipient, amount, connection)

    # отметить так же списание средств со счета
    if using_second_bill_number:
        await connection.fetchrow(
            add_wallet_operation(
                correlation_id,
                -amount,
                reason_id,
                wallet_id_sender,
                wallet_id_recipient
            )
        )
        await refresh_wallet_balance(wallet_id_sender, -amount, connection)


@transaction
async def payment_procces(connection, correlation_id: str, amount: float, reason_code: str, bill_number: str,
                          bill_number_sender: str = None):
    if await check_possibility_payment(correlation_id, connection):
        if bill_number_sender:
            balance = await get_wallet_field(bill_number_sender, 'balance', connection)
            if balance < amount:
                raise NotEnoughFunds(f'Not enough funds. Balance={balance}')
        await payment(connection, correlation_id, amount, reason_code, bill_number, bill_number_sender)

    else:
        raise OperationAlreadyExists(
            f'Payment operation already exists with correlation_id="{correlation_id}"'
        )
