#!/bin/bash

# Run database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn BlogBreeze.wsgi:application --bind=0.0.0.0:8000 --timeout 600 --workers 4
