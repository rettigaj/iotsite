from __future__ import print_function
"""
Django settings for iotsite project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)
eprint('PROJECT_DIR = {}'.format(PROJECT_DIR))
eprint('BASE_DIR = {}'.format(BASE_DIR))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'webpack_loader',   # react webpack integration
    'rest_framework',   # rest framework library
    'thorn.django',     # webhooks library
    'django_mysql',     # mysql support for API proxy
    'django_filters',   # field filtering for REST

    # custom apps
    'sensors',
    'external_api',
    'dashboard',
    #'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iotsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'iotsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

REST_FRAMEWORK = {
    #'PAGE_SIZE': 20,
    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework_csv.parsers.CSVParser'
    ],
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'ORDERING_PARAM': 'sort',

    #'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    #'DEFAULT_FILTER_BACKENDS': (
    #    'rest_framework_json_api.filters.QueryParameterValidationFilter',
    #    'rest_framework_json_api.filters.OrderingFilter',
    #    'rest_framework_json_api.django_filters.DjangoFilterBackend',
    #    'rest_framework.filters.SearchFilter',
    #),
    #'SEARCH_PARAM': 'filter[search]',
    #'TEST_REQUEST_RENDERER_CLASSES': (
    #    'rest_framework_json_api.renderers.JSONRenderer',
    #),
    #'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'
}

THORN_HMAC_SIGNER = 'thorn.utils.hmac:sign'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'assets'),
#]

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# DarkSky API CONF
if 'DARKSKY_KEY' in os.environ:
    DARKSKY_KEY = os.environ['DARKSKY_KEY']
    DARKSKY_LAT = os.environ['DARKSKY_LAT']
    DARKSKY_LON = os.environ['DARKSKY_LON']
    DARKSKY_THRESH = float(os.environ['DARKSKY_THRESH'])
else:
    eprint('DARKSKY_KEY Environment Variable is NOT set! Ignoring...')
    DARKSKY_KEY = 'NONE'
    DARKSKY_LAT = 'NONE'
    DARKSKY_LON = 'NONE'
    DARKSKY_THRESH = 'NONE'

# ignore system checks to support JSONField()
# https://github.com/adamchainz/django-mysql/issues/342
SILENCED_SYSTEM_CHECKS = [
    'django_mysql.E016',
]
