#!/bin/sh
echo "* * * * * python /app/manage.py clear_lobby  2>&1" > /etc/crontabs/root
echo "* * * * * python /app/manage.py clear_tournament 2>&1" >> /etc/crontabs/root
exec crond -f