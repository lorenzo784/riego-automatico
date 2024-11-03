#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn core.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4