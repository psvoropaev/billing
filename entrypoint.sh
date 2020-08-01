#!/bin/bash

exec alembic upgrade head
if [[ ${WORKER_MODE:-NO} = 'YES' ]]; then
    exec celery -A worker:app flower --port=5555 &
    exec celery -A worker:app worker -l=${LOG_LEVEL:-INFO} -n worker@%h --concurrency=${CONCURRENCY:-2} -P celery_pool_asyncio:TaskPool
else
  exec uvicorn main:app --host 0.0.0.0 --port 5000
fi