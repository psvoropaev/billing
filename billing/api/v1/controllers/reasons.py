from sqlalchemy import select

from billing import models, errors


async def get_reason_data(code: str, connection) -> tuple:
    """
    Get Reason id and second account participation flag
    :param code: unique reson code
    :param connection:
    :return reason_id, using_second_bill_number:
    """
    reason_query = select([
        models.reason.c.id,
        models.reason.c.using_second_bill_number
    ]).select_from(models.reason).where(models.reason.c.code == code)

    reason = await connection.fetchrow(reason_query)
    if reason and 'id' in reason and 'using_second_bill_number' in reason:
        return reason['id'], reason['using_second_bill_number']
    else:
        raise errors.NotFound(f'Reason not found with code="{code}"')
