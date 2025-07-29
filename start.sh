#!/bin/sh

# Ensure data directory exists
mkdir -p /app/data
chmod -R 777 /app/data

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start server
echo "Starting server..."
gunicorn --bind 0.0.0.0:8000 core.wsgi:application 