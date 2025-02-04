#!/bin/sh
echo $USER
python manage.py makemigrations && python manage.py migrate
python manage.py install
exec gunicorn -w 4 profile.wsgi.application -b 0.0.0.0

