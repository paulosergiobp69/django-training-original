#!/bin/bash

#run migrations
python manage.py migrate

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn xpence_project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120000