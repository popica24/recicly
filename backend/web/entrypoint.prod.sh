#!/bin/bash
set -e

echo "Starting entrypoint script..."

# If running as root, fix permissions and switch to reciclyuser
if [ "$(id -u)" = "0" ]; then
    echo "Running as root, fixing permissions..."
    mkdir -p /app/staticfiles
    chown -R reciclyuser:reciclyuser /app/staticfiles
    echo "Switching to reciclyuser..."
    exec su-exec reciclyuser "$0" "$@"
fi

echo "Running as reciclyuser ($(id -u))"

echo "Applying database migrations..."
uv run python manage.py migrate --noinput

# Harmless if nothing is collected.
echo "Collecting static files"
uv run python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec uv run gunicorn recicly.wsgi:application --bind 0.0.0.0:8000