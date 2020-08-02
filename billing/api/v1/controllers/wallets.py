from uuid import uuid4

from sqlalchemy import select, update

from billing import models, errors


def add_wallet(user_id: int, currency_id: int):
    """
    add wallet to db
    :param user_id: User
    :param currency_id: Currency
    :return:
    """
    return models.wallet.insert().values({
        'bill_number': str(uuid4()),
        'user_id': user_id,
        'balance': 0,
        'currency_id': currency_id
    })


async def get_wallet_field(bill_number: str, field: str, connection):
    """
    Get field value from wallet
    :param bill_number:
    :param field:
    :param connection:
    :return:
    """
    if not (field and bill_number):
        raise errors.BadParams(f'Wrong params, bill_number="{bill_number}", field="{field}"')

    wallet_query = select([
        models.wallet
    ]).select_from(models.wallet).where(models.wallet.c.bill_number == bill_number)

    wallet = await connection.fetchrow(wallet_query)
    if wallet and field in wallet:
        return wallet[field]
    else:
        raise errors.NotFound(f'Wallet not found with billing number="{bill_number}"')


async def refresh_wallet_balance(wallet_id: int, amount: float, connection) -> float:
    """
    Refresh wallet balance
    :param wallet_id:
    :param amount:
    :param connection:
    :return:
    """
    query_update = update(models.wallet).where(
        models.wallet.c.id == wallet_id
    ).values({'balance': models.wallet.c.balance + amount})
    await connection.fetch(query_update)