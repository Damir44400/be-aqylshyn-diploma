#!/bin/bash

ls -ld /app/media
chmod 777 /app/media
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000