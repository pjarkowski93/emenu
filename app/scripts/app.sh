#!/bin/bash -x

python manage.py crontab add
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
exec "$@"