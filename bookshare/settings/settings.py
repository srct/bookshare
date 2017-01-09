"""
Django settings for the bookshare project.
"""

# standard library imports
from __future__ import absolute_import, print_function, unicode_literals
import os
# core django imports
from django.contrib.messages import constants as messages
# imports from your apps
from . import secret

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# cryptography-- make this unique and don't share it with anybody.
SECRET_KEY = secret.SECRET_KEY

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'trades/templates'),
            os.path.join(BASE_DIR, 'core/templates'),
            os.path.join(BASE_DIR, 'lookouts/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        }
    }
]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'cas',
    # apps
    'trades',
    'core',
    'lookouts',
    'mod',
    # packages
    'crispy_forms',
    'django_gravatar',
    'haystack',
    'piwik',
    'randomslugfield',
    'storages',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MESSAGE_TAGS = {messages.ERROR: 'danger', }

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cas.middleware.CASMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'settings.urls'

WSGI_APPLICATION = 'settings.wsgi.application'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS
ORGANIZATION_EMAIL_DOMAIN = 'masonlive.gmu.edu'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secret.DB_NAME,
        'USER': secret.DB_USER,
        'PASSWORD': secret.DB_PASSWORD,
        'HOST': secret.DB_HOST,
        'PORT': secret.DB_PORT,
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend',
)

# Peoplefinder API for user creation
PF_URL = "https://api.srct.gmu.edu/pf/v1/"

CAS_SERVER_URL = 'https://login.gmu.edu'
CAS_LOGOUT_COMPLETELY = True
CAS_PROVIDE_URL_TO_LOGOUT = True
#LOGIN_URL = '/login/'
#LOGOUT_URL = '/logout/'

CAS_RESPONSE_CALLBACKS = (
    'core.cas_callbacks.create_user',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# Haystack Signal Processor
# The RealtimeSignalProcessor allows for objects to be indexed as soon as
# they are created --- in real time.
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Piwik configurations
PIWIK_SITE_ID = secret.PIWIK_SITE_ID
PIWIK_URL = secret.PIWIK_URL

# Email configurations
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = secret.EMAIL_HOST
EMAIL_PORT = '465'
EMAIL_HOST_USER = secret.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secret.EMAIL_HOST_PASSWORD

# Media configurations
MEDIA_S3 = False

if MEDIA_S3:
# Upload user files to AWS S3
    AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }

    AWS_STORAGE_BUCKET_NAME = secret.AWS_STORAGE_BUCKET_NAME
    AWS_ACCESS_KEY_ID = secret.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = secret.AWS_SECRET_ACCESS_KEY
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
else:
# Upload user files to your server; by default a /media directory
    MEDIA_URL = '/media/'
    MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))

# don't use redis when in develoment
if DEBUG:
    pass
else:
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '/var/run/redis/redis.sock',
        },
    }
