#!/bin/bash

while ! nc -zvw3 redis 6379; do echo waiting for Redis; sleep 3; done;
echo "Redis is up"

while ! nc -zvw3 postgres 5432; do echo waiting for Postgres; sleep 3; done;
echo "Postgres is up"

exec alembic upgrade head & uvicorn main:app --host 0.0.0.0 --port 5000
