#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] Running Django migrations..."
python manage.py migrate --noinput || { echo "Migration failed"; exit 1; }

echo "[entrypoint] Collecting static files..."
python manage.py collectstatic --noinput || { echo "Collectstatic failed"; exit 1; }

echo "[entrypoint] Starting gunicorn..."
exec gunicorn finisher_api.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 3 \
  --threads 2 \
  --timeout 120
