#!/usr/bin/env bash
pip install --upgrade pip
pip install gunicorn django djangorestframework drf-yasg django-cors-headers
python manage.py migrate