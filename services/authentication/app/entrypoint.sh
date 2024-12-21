#!/bin/sh
python manage.py makemigrations && python manage.py migrate ft_auth;
python manage.py runserver 0.0.0.0:8000