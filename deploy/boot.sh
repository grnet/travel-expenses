#!/bin/bash
cd /srv/travel/travelsBackend
echo "Starting migrate"
python manage.py migrate
echo "Filling Database with dummy data"
python manage.py loaddata texpenses/fixtures/data.json
python manage.py loadlocations texpenses/data/countriesTZ.csv
python manage.py loadtaxoffices texpenses/data/ListEfories.csv
python manage.py loaddata texpenses/fixtures/dummy_user_project_data.json
echo "Starting the server"
python manage.py runserver 0.0.0.0:8000
