#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e
echo "Starting Django application..."
# Apply database migrations and start the server
echo "running migrations..."
python manage.py migrate
echo "loading data..."
python manage.py loaddata dashboard/fixtures/data.json
echo "starting server..."
python manage.py runserver 0.0.0.0:8000