#!/usr/bin/env bash
set -x
cd /food-menu-voting
python manage.py makemigrations; python manage.py migrate
python manage.py createsuperuser --no-input --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

(cd /food-menu-voting; gunicorn voting_project.wsgi:application --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"