#!/bin/bash

set -e

echo "${0}: running migrations."
python manage.py makemigrations --merge
python manage.py migrate --noinput

echo "${0}: populating database."
python manage.py initdata

echo "${0}: collecting statics."
python manage.py collectstatic --noinput

echo "${0}: starting server."
gunicorn failaka.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=failaka.settings \
    --name failaka \
    --bind 0.0.0.0:8000 \
    --timeout 600 \
    --workers 4 \
    --log-level=info \
    --reload