#!/usr/bin/env bash
set -e

python manage.py db upgrade

gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 4 --timeout 0 project.server:app