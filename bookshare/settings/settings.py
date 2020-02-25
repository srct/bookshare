"""
Django settings for the bookshare project.
"""

# standard library imports
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
                'django.template.context_processors.request',
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
#    'api',
    # packages
    'crispy_forms',
    'django_gravatar',
    'haystack',
    'piwik',
    'randomslugfield',
    'rest_framework',
    'storages',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

MESSAGE_TAGS = {messages.ERROR: 'danger', }

MIDDLEWARE = (
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secret.DB_NAME,
        'USER': secret.DB_USER,
        'PASSWORD': secret.DB_PASSWORD,
        'HOST': secret.DB_HOST,
        'PORT': secret.DB_PORT,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Peoplefinder API for user creation
PF_URL = "https://api.srct.gmu.edu/pf/v1/"
ORGANIZATION_EMAIL_DOMAIN = 'masonlive.gmu.edu'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend',
)

CAS_SERVER_URL = 'https://login.gmu.edu/'
CAS_LOGOUT_COMPLETELY = True
CAS_PROVIDE_URL_TO_LOGOUT = True
# These fields are commented out because the views are
# specified directly in settings.urls
#LOGIN_URL = '/login'
#LOGOUT_URL = '/logout'

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
# the email address that error messages come from; sent to admins
ADMINS = (
         #('Bookshare Devs', 'bookshare@lists.srct.gmu.edu'),
         #('SRCT Execs', 'srct@gmu.edu'),
)
MANAGERS = ADMINS

USE_SES = False
if not USE_SES:
    if DEBUG:
        # print emails to the terminal where manage.py is running
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    else:
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = 'localhost'
        EMAIL_PORT = 25
        EMAIL_HOST_USER = secret.HOST_EMAIL_USER
        EMAIL_HOST_PASSWORD = secret.EMAIL_HOST_PASSWORD
        # includes implicit TLS
        EMAIL_USE_SSL = False
else:
    # configurations to send email via Amazon SES
    EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
    EMAIL_HOST = secret.SES_HOST
    EMAIL_PORT = '465'
    EMAIL_HOST_USER = secret.SES_USER
    EMAIL_HOST_PASSWORD = secret.SES_PASSWORD

# Media configurations
USE_S3 = False
if not USE_S3:
    # Upload user files to your server; by default a /media directory
    MEDIA_URL = '/media/'
    MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))
    # make sure to comment out line in settings/urls.py
else:
    # configurations to upload user media files to Amazon S3
    AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }

    AWS_STORAGE_BUCKET_NAME = secret.S3_BUCKET_NAME
    AWS_ACCESS_KEY_ID = secret.S3_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = secret.S3_SECRET_ACCESS_KEY
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % S3_STORAGE_BUCKET_NAME
    MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

if DEBUG:
    # dummy cache for development-- doesn't actually cache things
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        },
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            # configure to redis port
            'LOCATION': '/var/run/redis/redis.sock',
        },
    }

if not DEBUG:
    LOGGING = {
        'version': 1,
        # the ones the print everything out to the terminal
        # and the ones that email on SuspiciousOperation occurrences
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                # make sure to change this to the proper path, and one that
                # can be written to
                'filename': '/path/to/django/debug.log',
            },
            # 'mail_admins' by default does not include a traceback attachment
            # setting 'include_html' to True will attach an html traceback file to the email
            # you can also set an additional 'email_backend' arg to a custom email handler (e.g. SES)
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
            },
        },
        'loggers': {
            # logs request errors
            # 5XX responses are raised as ERROR messages
            # 4XX responses are raised as WARNING messages
            'django.request': {
                'handlers': ['file', 'mail_admins'],
                'propagate': True,
            },
            'django.template': {
                'handlers': ['file',],
                'propagate': True,
            },
        # django's default loggers send request and security messages at the ERROR
        # or CRITICAL level to the AdminEmailHandler via mail_admins
        },
    }
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console':{
                'level': 'DEBUG',
                'class': 'logging.StreamHandler'
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
