#!/usr/bin/env sh
# Sample start_app script used to start up celery task workers and run the app on port 8080
cd cnc
celery -A pan_cnc worker --loglevel=info &
python3 ./manage.py runserver 0.0.0.0:8080