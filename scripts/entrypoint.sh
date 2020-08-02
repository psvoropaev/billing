#!/bin/bash

while ! nc -zvw3 rabbitmq 5672; do echo waiting for RabbitMQ; sleep 3; done;
echo "RabbitMQ is up"

while ! nc -zvw3 postgres 5432; do echo waiting for Postgres; sleep 3; done;
echo "Postgres is up"


if [[ ${WORKER_MODE:-NO} = 'YES' ]]; then
    exec celery -A worker:celery_app flower --port=5555 &
    exec celery -A worker:celery_app worker -l=${LOG_LEVEL:-INFO} -n worker@%h --concurrency=${CONCURRENCY:-2} -P celery_pool_asyncio:TaskPool
else
  exec alembic upgrade head & uvicorn main:app --host 0.0.0.0 --port 5000
fi