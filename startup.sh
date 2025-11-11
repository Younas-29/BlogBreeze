#!/bin/bash

# Run database migrations
python manage.py migrate --noinput

# Collect static files  
python manage.py collectstatic --noinput

# Start Gunicorn on port 8000 (Azure App Service default for Python)
gunicorn BlogBreeze.wsgi:application --bind 0.0.0.0:8000 --timeout 600 --workers 4 --access-logfile '-' --error-logfile '-'
