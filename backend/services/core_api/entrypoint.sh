#!/bin/sh

# Останавливаем скрипт при любой ошибке
set -e

echo "Running database migrations..."
alembic upgrade head


echo "Starting FastAPI..."
exec uvicorn src.main:app --host 0.0.0.0 --port 80 --proxy-headers --forwarded-allow-ips '*' --root-path $ROOT_PATH