#!/bin/sh
echo "* * * * * python /app/manage.py clear_lobby  2>&1" > /etc/crontabs/root
echo "*/5 * * * * python /app/manage.py clear_tournament 2>&1" >> /etc/crontabs/root
echo "0 0 * * * python /app/manage.py anonymize_users 2>&1" >> /etc/crontabs/root
exec crond -f