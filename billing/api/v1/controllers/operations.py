import asyncio

from sqlalchemy import select

from billing import models
from billing.api.v1.controllers.reason import get_reason_data
from billing.api.v1.controllers.wallet import get_wallet_id


def add_wallet_operation(correlation_id: str, amount: float, reason_id: int, wallet_id_recipient: int,
                         wallet_id_sender: int=None):
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
            bill_num_sender: str=None):
    reason_id, using_second_bill_number = await get_reason_data(reason_code, connection)
    wallet_id_recipient = await get_wallet_id(bill_num_recipient, connection)
    wallet_id_sender = await get_wallet_id(bill_num_sender, connection) if using_second_bill_number else None

    tasks = []
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