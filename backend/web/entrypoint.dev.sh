#!/bin/bash
set -e

echo "Starting entrypoint script..."

echo "Applying database migrations..."
uv run python manage.py migrate --noinput

echo "Starting Local Server..."
uv run python manage.py runserver --insecure 0.0.0.0:8000
