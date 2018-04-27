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
# Build paths inside the dir manage commands are run from.
BASE_DIR = os.path.abspath(os.getcwd())


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '26ch88!x45adfwl4-6vuh6@3z^-@8#^b8#a@)ty(tp^)1!za*x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = DEBUG

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
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
PAGINATION_PAGE_SIZE = 0
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
}
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': API_PREFIX + '/auth/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': API_PREFIX + '/auth/activate/{uid}/{token}',
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
        'NAME': os.path.join(BASE_DIR, 'mydb.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
# TIME_ZONE = 'Europe/Athens'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

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


# Logging configuration
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
            'filename': os.path.join(BASE_DIR, 'travelexpenses.log'),
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

# Path to resources file.
RESOURCES_FILE = os.path.join(BASE_DIR,'../resources/common.json')
try:
    from local_settings import *
except ImportError, e:
    pass