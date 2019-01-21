#!/bin/bash
cd /srv/travel/travelsFront
echo "Starting ember build"
ember build --watch --dev &
cd /srv/travel/travelsBackend
echo "Starting migrate"
python manage.py migrate
echo "Filling Database with dummy data"
python manage.py loaddata texpenses/fixtures/data.json
python manage.py loadlocations texpenses/data/countriesTZ.csv
python manage.py loadprojects texpenses/data/ListProjects.csv
python manage.py loadtaxoffices texpenses/data/ListEfories.csv
echo "Starting the server"
python manage.py runserver 0.0.0.0:8000
