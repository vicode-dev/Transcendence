#!/bin/sh
python manage.py makemigrations && python manage.py migrate app
exec daphne app.asgi:application -b 0.0.0.0 -p 8000

