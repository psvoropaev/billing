import functools
import logging

from asyncpg.pool import Pool, PoolConnectionProxy
from asyncpgsa.pool import create_pool

from billing.app.config import config

logger = logging.getLogger(config.APP_NAME)


class DBPool:
    db_pool = None

    @classmethod
    async def init_db(cls):
        pool = await create_pool(dsn=config.DB_PG_URL, min_size=3)
        cls.db_pool = pool

    @classmethod
    async def close_db(cls):
        await cls.db_pool.close()

    @classmethod
    async def get_pool(cls):
        return cls.db_pool


db_pool_shared = DBPool()


def dbpool(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        if 'db_pool' not in kwargs and all(not isinstance(arg, Pool) for arg in args):
            pool = await db_pool_shared.get_pool()
            return await f(*args, db_pool=pool, **kwargs)
        else:
            return await f(*args, **kwargs)

    return wrapper


def transaction(f):
    @dbpool
    async def wrapper(*args, db_pool, **kwargs):
        if 'connection' not in kwargs and all(not isinstance(arg, PoolConnectionProxy) for arg in args):
            async with db_pool.acquire() as conn:
                tran = conn.transaction()
                try:
                    await tran.start()
                    result = await f(*args, connection=conn, **kwargs)
                    await tran.commit()
                    return result
                except Exception as e:
                    await tran.rollback()
                    logger.exception(e)
                    raise e
        else:
            return await f(*args, **kwargs)
    return wrapper
