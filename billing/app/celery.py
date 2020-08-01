import celery.signals

from billing.app.config import config


app = celery.Celery(
    'billing',
    broker=config.CELERY_BROKER_URL,
    worker_hijack_root_logger=False,
    include=[
        'billing.api.v1.controllers.tasks',
    ]
)

# celery.signals.before_task_publish.connect(tracing.celery.before_task_publish)
# celery.signals.task_prerun.connect(tracing.celery.preprocess_task)
# celery.signals.task_postrun.connect(tracing.celery.preprocess_task)