#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e
echo "Starting Django application..."
# Apply database migrations and start the server
echo "running migrations..."
python manage.py migrate
echo "collecting static files..."
python manage.py collectstatic --noinput
echo "starting server..."
python manage.py runserver