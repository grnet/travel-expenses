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

MAX_HOLIDAY_DAYS = 60
HOST_URL = "http://localhost:8000/"
API_PREFIX = "api"
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'texpenses',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_tracking',
    'djoser',
    'crispy_forms',
    'rest_framework_docs',
)
REST_FRAMEWORK = {
    # 'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%S",
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M",
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'auth/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': API_PREFIX+'/auth/activate/{uid}/{token}',
    'PASSWORD_VALIDATORS': [],
    'SERIALIZERS': {},
    'SEND_ACTIVATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'SITE_NAME': 'GRNET Travel Expenses',
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
}

MIDDLEWARE_CLASSES = (
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

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Athens'
# DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

USE_I18N = True

USE_L10N = True

USE_TZ = False


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
        }
    }
}


# useful trick for custom settings
try:
    from local_settings import *
except ImportError, e:
    pass
