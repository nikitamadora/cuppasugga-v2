#!/bin/bash
source /tmp/cuppasugga-env/bin/activate
cd "$(dirname "$0")"
DJANGO_SETTINGS_MODULE=cuppasugga.local_settings python manage.py runserver
