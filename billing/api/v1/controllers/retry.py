import asyncio
import logging
import functools

from sqlalchemy.exc import SQLAlchemyError

from billing.app.config import config
from billing.app.redis import cache_data_payments, del_cache_data_payments

logger = logging.getLogger(config.APP_NAME)


def autoretry(
        delay_attempts=config.DELAY_ATTEMPTS,
        autoretry_for=(SQLAlchemyError, )
):
    """
    Autoretry for functions, catching exceptions "autoretry_for"
    """

    def decorator(f):
        @functools.wraps(f)
        async def wrapper(*args, correlation_id, **kwargs):
            for i, sleep_value in enumerate(delay_attempts):
                try:
                    await cache_data_payments(*args, correlation_id=correlation_id, **kwargs)
                    return await f(*args, str(correlation_id), **kwargs)
                except autoretry_for as ex:
                    if i == len(delay_attempts):
                        logger.error(f'Excess max retry count: {f.__name__}__{len(delay_attempts)}')
                        await asyncio.sleep(sleep_value)
                    logger.exception(ex)
                except Exception as ex:
                    logger.exception(ex)
                    await del_cache_data_payments(correlation_id=correlation_id)
                    raise ex
            await del_cache_data_payments(correlation_id=correlation_id)

        return wrapper

    return decorator
