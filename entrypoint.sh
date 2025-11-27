#!/bin/bash

echo "Starting..."

# Make logs folder
mkdir -p logs


lsof -ti :8001 | xargs kill -9 2>/dev/null || true
sleep 3

# Run migrations
python manage.py migrate --noinput

# Collect static
python manage.py collectstatic --noinput --clear



echo "Services started!"

# Start gunicorn (stays running)
gunicorn zerazone.wsgi:application --bind 0.0.0.0:8001 --workers 1