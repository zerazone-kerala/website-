#!/bin/bash

echo "Starting..."

# Make logs folder
mkdir -p logs

# Kill old processes
pkill -9 celery
lsof -ti :8686 | xargs kill -9 2>/dev/null || true
sleep 3

# Run migrations
python manage.py migrate --noinput

# Collect static
python manage.py collectstatic --noinput --clear

# Start celery worker
celery -A luminar_website worker --loglevel=info --logfile=logs/celery.log &
sleep 5

# Start celery beat
celery -A luminar_website beat --loglevel=info --logfile=logs/beat.log &
sleep 2

echo "Services started!"

# Start gunicorn (stays running)
gunicorn luminar_website.wsgi:application --bind 0.0.0.0:8686 --workers 2