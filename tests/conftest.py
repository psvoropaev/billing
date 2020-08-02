import pytest
import asyncio

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from asyncpgsa.pool import create_pool
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig

from billing.app import create_app
from billing.app.config import config
from billing.models import user, wallet, operation

ALEMBIC_CONFIG = 'alembic.ini'


def pytest_pycollect_makeitem(collector, name, obj):
    """
    Fix pytest collecting for coroutines.
    Or mark 'async def' functions by '@pytest.mark.asyncio' explicitly
    """
    if collector.funcnamefilter(name) and asyncio.iscoroutinefunction(obj):
        obj = pytest.mark.asyncio(obj)
        return list(collector._genfunctions(name, obj))


@pytest.fixture(autouse=True, scope='session')
def init_and_clear_db():
    alembic_config = AlembicConfig(ALEMBIC_CONFIG)
    alembic_config.attributes['configure_logger'] = False

    upgrade(alembic_config, 'head')

    yield 'on head'

    connectable = create_engine(config.DB_PG_URL)
    with connectable.connect() as conn:
        conn.execute(operation.delete())
        conn.execute(wallet.delete())
        conn.execute(user.delete())

    downgrade(alembic_config, 'base')


@pytest.fixture(scope='function')
def client():
    return TestClient(create_app())


@pytest.fixture(scope='function')
def db_pool(event_loop):
    pool = create_pool(config.DB_PG_URL)
    event_loop.run_until_complete(pool)

    try:
        yield pool
    finally:
        event_loop.run_until_complete(pool.close())


@pytest.fixture(scope='function')
def db_conn(db_pool, event_loop):
    conn = event_loop.run_until_complete(db_pool.acquire())
    try:
        yield conn
    finally:
        event_loop.run_until_complete(db_pool.release(conn))
