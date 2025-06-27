#!/bin/bash
set -e

echo "Starting entrypoint script..."

echo "Applying database migrations..."
uv run python manage.py migrate --noinput

# Harmless if nothing is collected.
echo "Collecting static files"
uv run python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec uv run gunicorn comparator.wsgi:application --bind 0.0.0.0:8000
