#!/bin/bash
set -e

while ! nc -z db 5432; do sleep 1; done
sleep 2

cd /wallet

poetry run alembic upgrade head

exec poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
