#!/bin/sh
echo $USER
python manage.py makemigrations && python manage.py migrate;
python manage.py install;
exec python manage.py runserver 0.0.0.0:8000