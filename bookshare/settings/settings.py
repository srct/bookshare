# Django settings for bookshare project.

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'trades/templates'),
    os.path.join(BASE_DIR, 'core/templates'),
    os.path.join(BASE_DIR, 'lookouts/templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'trades',
    'core',
    'lookouts',
    'django_gravatar',
    'crispy_forms',
    'easy_thumbnails',
    'haystack',
    'piwik',
    'django.contrib.admindocs',
)

CRISPY_TEMPLATE_PACK = 'bootstrap'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cas.middleware.CASMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'settings.urls'

WSGI_APPLICATION = 'settings.wsgi.application'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS
ORGANIZATION_EMAIL_DOMAIN = 'masonlive.gmu.edu'

import secret
SECRET_KEY = secret.SECRET_KEY

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

SITE_ID = 1

TIME_ZONE = 'America/New_York'

ALLOWED_HOSTS = ['127.0.0.1']

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

STATIC_URL = '/static/'

THUMBNAIL_ALIASES = {'': {
    'listing_photo': {
        'size': (333, 250),
        'crop': True,
    },
},}

MEDIA_URL = '/media/'
MEDIA_ROOT = (os.path.join(BASE_DIR, 'media/'))
MEDIAFILES_DIRS = (
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend',
)

CAS_SERVER_URL = 'https://login.gmu.edu'
CAS_LOGOUT_COMPLETELY = True
CAS_PROVIDE_URL_TO_LOGOUT = True
#LOGIN_URL = '/login/'
#LOGOUT_URL = '/logout/'

CAS_RESPONSE_CALLBACKS = (
    'core.cas_callbacks.create_user',
)

HAYSTACK_CONNECTIONS = {
    'default' : {
        'ENGINE' : 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH' : os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# Haystack Signal Processor
# The RealtimeSignalProcessor allows for objects to be indexed as soon as
# they are created --- in real time.
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Piwik configurations
PIWIK_SITE_ID = secret.PIWIK_SITE_ID
PIWIK_URL = secret.PIWIK_URL
