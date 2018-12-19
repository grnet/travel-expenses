# Travel Expenses

The electronic service [Travel Expenses](https://travelexpenses.grnet.gr/ui/auth/login) provides an easy way to manage professional trips and generates all the required documents for the user's compensation.

## Prerequisites

* Python 2.7
* git
* pip
* NodeJS
* Yarn

On a Debian Stretch system, the following packages are also required:
* libcairo2
* libpango-1.0-0
* pangocairo-1.0
* libffi-dev

## Development Instructions

### Backend installation

#### Getting the repo and installing dependencies

* Clone this repo and checkout to `develop` branch
* Install python dependencies (it's highly recommended to use a virtualenv)
```
$ pip install -r requirements.txt
```

#### Configuration

* Create a `settings.conf` file. The default path for it is `/etc/travel`. The path can be overriden by setting the `TRAVEL_SETTINGS_DIR` shell variable. This file overrides Django's `settings.py` and it should contain at least the following lines (change IP accordingly):
```
ALLOWED_HOSTS = [u'SERVICE.IP.HERE']
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = DATA_DIR
```
Consider also setting `DEBUG` and `TEMPLATE_DEBUG` to True.

* The service expects a resources directory at `/usr/lib/travel/resources`. Those resources can be found in the resources directory in the root folder of the repo. The path can be overriden by setting the `APELLA_RESOURCES_DIR` shell variable.

#### Database initialization

* Initialize database
```
$ python manage.py migrate
```

#### Running the server

* Use the following command:
```
$ python manage.py runserver
```
You can now view your api at [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

#### Adding dummy data (Optional)

* To add dummy data to the database run the following commands:
```
$ python manage.py loaddata texpenses/fixtures/data.json
$ python manage.py loadlocations texpenses/data/countriesTZ.csv
$ python manage.py loadprojects texpenses/data/ListProjects.csv
$ python manage.py loadtaxoffices texpenses/data/ListEfories.csv
```
