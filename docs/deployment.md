Deployment instructions
=======================

This guide demonstrates instructions on how to deploy Travel Expenses application. These instructions were tested on Debian Jessie.

Requirements
------------

-	nginx
-	postgresql
-	gunicorn
-	git
-	django
-	ember-cli
-	certificates to establish TLS connection
-	nodejs and npm

### Install all required packages:

```
export LC_ALL="en_US.UTF-8" # Postgres installation failed.
apt-get update
apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib nginx\
    git gunicorn curl python-lxml python-cffi libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0 shared-mime-info memecached
```

Configure Postgres
------------------

To work with Postgres in its default configuration, it is best to change to the postgres system user temporarily. Do that now by typing:

`sudo su - postgres`

When operating as the postgres user, you can log right into a PostgreSQL interactive session with no further authentication by typing:

`psql`

First, create a database for your project:

```sql
CREATE DATABASE travelproduction;
```

Next, create a database user for our project:

```sql
CREATE USER traveluser WITH PASSWORD 'travelpassword';
```

We are setting the default encoding to UTF-8, which Django expects. We are also setting the default transaction isolation scheme to "read committed", which blocks reads from uncommitted transactions. Lastly, we are setting the timezone. Finally, our Django project will be set to use Europe/Athens:

```sql
ALTER ROLE traveluser SET client_encoding TO 'utf8';
ALTER ROLE traveluser SET default_transaction_isolation TO 'read committed';
ALTER ROLE traveluser SET timezone TO 'Europe/Athens';
```

Now, all we need to do is give our database user access rights to the database we created:

```sql
GRANT ALL PRIVILEGES ON DATABASE travelproduction TO traveluser;
```

Exit the SQL prompt to get back to the postgres user's shell session:

`\q`

Exit out of the postgres user's shell session to get back to your regular user's shell session:

`exit`

Get Application code
--------------------

We first decide where application will be located, in our example at `/srv/` Then, we have to get code of our application from the corresponding phab repo.

```
cd /srv/
git clone ssh://phab-vcs-user@phab.dev.grnet.gr:222/diffusion/TRAVEL/travel-expenses-repo.git
cd travel-expenses-repo
git checkout <your branch>
```

Deploy Backend
--------------

### Configure application

First install application's required packages.

```
cd travelsBackend
pip install -U pip
pip install -r requirements.txt
apt-get install python-psycopg2
```

Then, we should configure our application e.g. database, static, etc. We create a file called `local_settings.py`.

Firstly,

Replace block:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'mydb.sqlite3'),
    }
}
```

with:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'travelproduction',
        'USER': 'traveluser',
        'PASSWORD': 'travelpassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

and secondly add the following lines of code:

```
SECRETARY_EMAIL = 'secretary@admin.grnet.gr'
MAX_HOLIDAY_DAYS = 60
HOST_URL = "https://travel.admin.grnet.gr/"
API_PREFIX = "api"
DEBUG = False
TEMPLATE_DEBUG = DEBUG
ENUM_FILE='/srv/travel-expenses-repo/resources/common.json'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'grnet.travel.expenses@gmail.com'
EMAIL_HOST_PASSWORD = 'd\\M^mp2\\[4~UX\'"Y'
EMAIL_PORT = 587
SERVER_EMAIL = 'grnet.travel.expenses@gmail.com'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

STATIC_URL = '/static_production/'
STATIC_ROOT='/srv/travel-expenses-repo/travelsBackend/static_production/'

MEDIA_ROOT = 'uploads'
MEDIA_URL = HOST_URL + MEDIA_ROOT + '/'
```

### Caching configuration

In order to customize the caching configuration change the following attributes located at `setting.py` file:

```
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_ERRORS': False,
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60
}
```

`LOCATION`: is the IP and PORT where the MemcachedCache is running. The common values are the one already used (`127.0.0.1:11`\)

`DEFAULT_CACHE_ERRORS`: Disable REST Framework error responses caching.

`DEFAULT_CACHE_RESPONSE_TIMEOUT`: Use this attribute to define caching time.

The last thing we have to do is to migrate the initial database schema and data to our PostgreSQL database, as well as to create `static_(parent_folder)` where all static files are stored ..

```
python manage.py migrate
python manage.py loaddata texpenses/fixtures/data.json
python manage.py loadlocations --delete texpenses/data/countries.csv
python manage.py loadprojects --delete texpenses/data/ListProjects.csv
python manage.py loadtaxoffices texpenses/data/ListEfories.csv
python manage.py collectstatic
```

### Configure Gunicorn

In order to run our project (WSGI application) through gunicorn, we will create a gunicorn startup script (WSGI) at `/etc/gunicorn.d/texpenses`

```python
CONFIG = {
    'mode': 'wsgi',
    'environment': {
        'PYTHONPATH':'/srv/travel-expenses-repo/travelsBackend/'
    },
    'working_dir': '/srv/data/',
    'args': (
        '--log-level=debug',
        '--log-file=/var/log/gunicorn/texpenses.log',
        '--bind=127.0.0.1:8001',
        '--workers=2',
        '--reload',
        'travelsBackend.wsgi:application',
    ),
```

In the script above, we set the gunicorn `working_dir` where the backend code is located. At the `args` section we define the `--log-level`, the location (`--log-file`) where the log files will be stored, the URL binding (in our case at localhost see next section), number of worker threads ( `workers` ), option to reload every time th e backend code changes and the WSGI application file.

The script above will also run automatically after host restarts.

**Start gunicorn:**

```shell
/etc/init.d/gunicorn start
```

Check whether everything went well:

```
tail -f /var/log/gunicorn/texpenses.log
```
### Configure Crontabbed jobs
In local `local_settings.py` file insert the following in case you want to override the system defaults.

```python
CRONJOBS = [
    ('*/1 * * * *', 'texpenses.actions.compensation_alert',
     '>> /path_to_save/scheduled_job.log')
]
```
For more info on how to setup crontab check [this wiki](https://en.wikipedia.org/wiki/Cron#Format).
After configuration just run on terminal:

```bash
python manage.py crontab add
```

for removing Travel Expenses jobs from crontab run on the following on terminal:

```bash
python manage.py crontab remove
```
Finally in order to show all Travel Expenses jobs run the following on terminal:

```bash
python manage.py crontab show
```

### Configure Nginx

If we are done with gunicorn we are ready to configure Nginx proxy server. As mentioned at the previous section, gunicorn serves the Travel Expenses Backend at localhost level, meaning that it is not accessible to the outer world. In order to do so in a safe manner, we will use [nginx](https://nginx.org/en/) , an HTTP and reverse proxy server, a mail proxy server, and a generic TCP/UDP proxy server. Nginx is already installed so we will just configure it in order to serve our application.

Create a configuration file at: `/etc/nginx/sites-available/travel`

```
# Redirect to https.
server {
    listen 80 default_server;
    listen [::]:80 default_server ipv6only=on;
    server_name travel.admin.grnet.gr
    location / {
            rewrite ^(.*)   https://travel.admin.grnet.gr$1;
    }

    index index.html index.html;
}
server {
    listen 443 ssl;
    server_name travel.admin.grnet.gr;

    root /srv/web/travel.admin.grnet.gr;
    index index.html index.htm;

    ssl_certificate /etc/ssl/certs/travel_admin_grnet_gr.pem;
    ssl_certificate_key /etc/ssl/private/travel.admin.grnet.gr.key;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static_production/ {
            root /srv/travel-expenses-repo/travelsBackend;
     }
    location /uploads/ {
            root /srv/data/;
     }

    location /api {
        proxy_pass http://127.0.0.1:8001/api;
                proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    location /admin {
        proxy_pass http://127.0.0.1:8001/admin;
                proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        include /etc/nginx/travel_whitelist.conf;

        deny all;    

    }
```

The `include /etc/nginx/travel_whitelist.conf` declaration defines a white list configuration file. Inside there you just have to insert the IP address of the client that is permitted to access the Travel Expenses Admin page.

Create a symbolic link:

```
ln /etc/nginx/sites-available/travel /etc/nginx/sites-enabled/
```

**Restart nginx:**

```
/etc/init.d/nginx restart
```

For more info on nginx configuration options please check the [nginx documentation wiki](https://www.nginx.com/resources/wiki/)

Deploy frontend
---------------

### Install npm

```
apt-get install apt-transport-https lsb-release curl
curl -s https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add -
echo 'deb https://deb.nodesource.com/node_4.x jessie main' > /etc/apt/sources.list.d/nodesource.list
echo 'deb-src https://deb.nodesource.com/node_4.x jessie main' >> /etc/apt/sources.list.d/nodesource.list
apt-get update && apt-get install nodejs
```

### Install frontend dependencies

```
cd /var/travel-expenses-repo/travelsFront
npm install -g bower ember-cli
npm install && bower install
```

### Configure frontend

In `config/environment.js` use the correct value for:

```
var API_EP = "https://travel.admin.grnet.gr/api";
```

### Build frontend code

Run the following command:

```
ember build -prod
```

### Configure ngnix

Add the following to the existing configuration to server frontend application, so that the `/etc/nginx/sites-available/travel` looks like:

```
# Redirect to https.
server {
    listen 80 default_server;
    listen [::]:80 default_server ipv6only=on;
    server_name travel.admin.grnet.gr
    location / {
            rewrite ^(.*)   https://travel.admin.grnet.gr$1;
    }

    index index.html index.html;
}

server {
    listen 443 ssl;
    server_name travel.admin.grnet.gr;

    root /srv/web/travel.admin.grnet.gr;
    index index.html index.htm;

    ssl_certificate /etc/ssl/certs/travel_admin_grnet_gr.pem;
    ssl_certificate_key /etc/ssl/private/travel.admin.grnet.gr.key;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
            root /var/travel-expenses-repo/travelsBackend;
     }

    location /api {
        proxy_pass http://127.0.0.1:8001/api;
                proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    location ~ /ui/assets/(.*) {
                alias /var/travel-expenses-repo/travelsFront/dist/assets/$1;
    }
    location ~ /ui/$ {
                alias /var/travel-expenses-repo/travelsFront/dist/;
    }
    location ~ /ui/.* {
                alias /var/travel-expenses-repo/travelsFront/dist/index.html;
                add_header Content-Type text/html;
    }
}
```

That's all! Access login page of app at [https://travel.admin.grnet.gr/ui/login](https://travel.admin.grnet.gr/ui/login)
