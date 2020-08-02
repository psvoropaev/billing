import asyncio
import logging
import functools

from sqlalchemy.exc import SQLAlchemyError

from billing.app.config import config
from billing.app.redis import cache_data_payments, del_cache_data_payments
from billing.errors import MaxRetryCount

logger = logging.getLogger(config.APP_NAME)


def autoretry(
        delay_attempts=config.DELAY_ATTEMPTS,
        autoretry_for=(SQLAlchemyError,),
        excess_retry_exception=MaxRetryCount
):
    """
    Autoretry for functions, catching exceptions "autoretry_for"
    """

    def decorator(f):
        @functools.wraps(f)
        async def wrapper(*args, correlation_id, **kwargs):
            try:
                for i in delay_attempts:
                    try:
                        await cache_data_payments(*args, correlation_id=correlation_id, **kwargs)
                        return await f(*args, correlation_id, **kwargs)
                    except autoretry_for as ex:
                        if f.retry_count == len(delay_attempts):
                            logger.error(f'Excess max retry count: {len(delay_attempts)}')
                            raise excess_retry_exception(f'Excess max retry count for {f.__name__}')
                        else:
                            logger.exception(ex)
                            await asyncio.sleep(i)
            except Exception as ex:
                logger.exception(ex)
            await del_cache_data_payments(correlation_id=correlation_id)

        return wrapper

    return decorator
