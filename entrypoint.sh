#!/bin/sh

echo "Waiting for Database ..."
while ! nc -z mongodb 27017; do
  sleep 0.1
done

echo "Database started"

uwsgi --http-socket 0.0.0.0:5000 --wsgi-file wsgi.py --callable application --processes 4