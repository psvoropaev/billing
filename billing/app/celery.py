from celery import Celery
from celery.signals import worker_init, worker_shutting_down
import celery_decorator_taskcls
import celery_pool_asyncio

from billing.app.config import config
from billing.app.pg import db_pool_shared

celery_pool_asyncio.__package__
celery_decorator_taskcls.patch_celery()

celery_app = Celery(
    'billing',
    broker=config.CELERY_BROKER_URL,
    worker_hijack_root_logger=False,
    worker_pool=celery_pool_asyncio.TaskPool,
    include=[
        'billing.api.v1.controllers.tasks',
    ]
)


@worker_init.connect
async def do_startup_async(sender, **kwargs):
    await db_pool_shared.init_db()


@worker_shutting_down.connect
async def do_shutdown(sender=None, **kwargs):
    await db_pool_shared.close_db()
