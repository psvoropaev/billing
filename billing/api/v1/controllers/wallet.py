from uuid import uuid4

from sqlalchemy import select

from billing import models, errors


def add_wallet(user_id: int):
    return models.wallet.insert().values({
        'bill_number': str(uuid4()),
        'user_id': user_id,
        'balance': 0
    })


async def get_wallet_field(bill_number: str, field: str, connection) -> int:
    wallet_query = select([
        models.wallet
    ]).select_from(models.wallet).where(models.wallet.c.bill_number == bill_number)

    wallet = await connection.fetchrow(wallet_query)
    if wallet and field in wallet:
        return wallet[field]
    else:
        raise errors.NotFound(f'Wallet not found with billing number="{bill_number}"')
