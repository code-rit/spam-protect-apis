#!/bin/bash

# Specify the directory path
CELERY_LOG_DIRECTORY="logs/celery-logs"
UWSGI_LOG_DIRECTORY="logs/uwsgi-logs"

if [ ! -d "$CELERY_LOG_DIRECTORY" ]; then
	mkdir -p "$CELERY_LOG_DIRECTORY"
fi

if [ "$DEPLOYMENT_TYPE" = "PRODUCTION" -o "$DEPLOYMENT_TYPE" = "STAGING" ]; then
	if [ ! -d "$UWSGI_LOG_DIRECTORY" ]; then
		mkdir -p "$UWSGI_LOG_DIRECTORY"
	fi
	python manage.py collectstatic --noinput
	tail -f /dev/null #Keeps the docker container running
else
	python3 manage.py runserver 0.0.0.0:8000
fi
