#!/bin/bash
cd /srv/travel/travelsFront
ember build --watch --dev &
cd /srv/travel/travelsBackend
python manage.py migrate
echo "Filling Database with dummy data"
python manage.py runserver 0.0.0.0:8000
