#!/bin/sh
python manage.py makemigrations && python manage.py migrate ft_auth
exec gunicorn -w 4 -b 0.0.0.0 ft_auth.wsgi:application
