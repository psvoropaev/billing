import asyncio
import logging
import functools

from sqlalchemy.exc import SQLAlchemyError, ArgumentError

from billing.app.config import config
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
        async def wrapper(*args, **kwargs):
            try:
                logger.error('111111111111111111111111111111')
                raise ArgumentError('ooooooooooooooooooooooooo')
                return await f(*args, **kwargs)
            except autoretry_for as ex:
                if self.request.retries == config.COUNT_ATTEMPTS:
                    logger.error(f'Excess max retry count: {len(delay_attempts)}')
                    raise excess_retry_exception(f'Excess max retry count for {f.__name__}')
                self.retry(countdown=config.DELAY_ATTEMPTS, max_retries=config.COUNT_ATTEMPTS, exc=ex)

        return wrapper

    return decorator
