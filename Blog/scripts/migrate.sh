#!/bin/sh
makemigrations.sh
echo 'Execute migrate.sh'
python manage.py migrate --noinput