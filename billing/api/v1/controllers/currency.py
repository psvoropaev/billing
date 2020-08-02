from sqlalchemy import select

from billing import models, errors


async def get_currency_id(code: str, connection) -> int:
    """
    Get currency_id by code
    :param code - unique currency code:
    :param connection:
    :return: currency_id
    """
    currency_query = select([
        models.currency.c.id
    ]).select_from(models.currency).where(models.currency.c.alias == code)

    currency = await connection.fetchrow(currency_query)
    if currency and 'id' in currency:
        return currency['id']
    else:
        raise errors.NotFound(f'Currency not found with code="{code}"')
