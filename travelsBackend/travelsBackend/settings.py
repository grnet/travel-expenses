#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings for travelsBackend project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '26ch88!x45adfwl4-6vuh6@3z^-@8#^b8#a@)ty(tp^)1!za*x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []
TEMPLATE_DIRS = ()
DEFAULT_CITY_DB_ID = 4269
BASE_COUNTRY = u'Ελλάδα'
GOOGLE_MAPS_KEY = '***REMOVED***'

MEDIA_ROOT = 'uploads'
MAX_HOLIDAY_DAYS = 60
SECRETARY_EMAIL = 'test@email.com'
CONTROLLER_EMAIL = 'controller@email.com'

DEFAULT_CURRENCY = 'EUR'
HOST_URL = "http://localhost:8000/"
# MEDIA_URL = HOST_URL + MEDIA_ROOT + '/'
MEDIA_URL = '/TRAVEL/'
API_PREFIX = "api"
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'texpenses',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_crontab',
)
CRONJOBS = [
    ('0 0 * * *', 'texpenses.actions.compensation_alert',
     '>> /home/kostas/travelRepo/travelsBackend/logs/scheduled_job.log')
]
PAGINATION_PAGE_SIZE = 0
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
}
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'ui/auth/login#reset={uid}|{token}',
    'ACTIVATION_URL': 'ui/auth/login#activate={uid}|{token}',
    'PASSWORD_VALIDATORS': [],
    'SERIALIZERS': {},
    'SEND_ACTIVATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'SITE_NAME': 'GRNET Travel Expenses',
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
}

MIDDLEWARE_CLASSES = (
    'texpenses.middleware.ExceptionLoggingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'travelsBackend.urls'

WSGI_APPLICATION = 'travelsBackend.wsgi.application'

AUTH_USER_MODEL = 'texpenses.UserProfile'
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  './mydb.sqlite3',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
# TIME_ZONE = 'Europe/Athens'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
DATE_FORMAT_WITHOUT_TIME = '%Y-%m-%d'

USE_I18N = True


#===Create migrations on value changes===
DECIMAL_MAX_DIGITS = 8
DECIMAL_PLACES = 2
#=======================================
DECIMAL_SEPARATOR = ','

# A workaround setting for translations bug [1]
# [1] https://code.djangoproject.com/ticket/24569
USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

LOGFILE = os.environ.get('TRAVEL_LOGFILE', '/var/log/travel/travelexpenses.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s\
            %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGFILE,
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'texpenses': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO'
        },
        'django_crontab': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'DEBUG'
        },
        # 'django.db': {
            # 'handlers': ['console', 'mail_admins', 'file'],
            # 'level': 'DEBUG'
        # }

    }
}

RESOURCES_DIR = os.environ.get('TRAVEL_RESOURCES_DIR',
        '/usr/lib/travel/resources')
RESOURCES_FILE = os.path.join(RESOURCES_DIR, 'common.json')

SETTINGS_DIR = os.environ.get('TRAVEL_SETTINGS_DIR', '/etc/travel')
SETTINGS_FILE = 'settings.conf'
SETTINGS_PATH = os.path.join(SETTINGS_DIR, SETTINGS_FILE)

if not os.path.isfile(SETTINGS_PATH):
    m = "Cannot find settings file {0!r}. Consider using TRAVEL_SETTINGS_DIR "
    m += "environment variable to set a custom path for settings.conf file."
    m = m.format(SETTINGS_PATH)
    raise RuntimeError(m)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(RESOURCES_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]


execfile(SETTINGS_PATH)

try:
    from local_settings import *
except ImportError, e:
    pass
