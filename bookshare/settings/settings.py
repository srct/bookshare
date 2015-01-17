# Django settings for bookshare project.

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
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
    'website',
    'bids',
    'lookouts',
    'easy_thumbnails',
    'haystack',
    'piwik',
    'django.contrib.admindocs',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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

STATIC_URL = '/static/'

ACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'

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

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/'

# Authentication
# http://pythonhosted.org/django-auth-ldap

import ldap
# Baseline configuration

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_SERVER_URI = "ldaps://directory.gmu.edu:636"  # server url

AUTH_LDAP_BIND_DN = "ou=people,o=gmu.edu"               # bind DN

AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True            # use the user

AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=people,o=gmu.edu"

AUTH_LDAP_GLOBAL_OPTIONS = {                            # ignore UAC cert.
    ldap.OPT_X_TLS : ldap.OPT_X_TLS_DEMAND,
    ldap.OPT_X_TLS_REQUIRE_CERT : ldap.OPT_X_TLS_NEVER,
}

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}
#AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#    "is_active": "cn=active,ou=django,ou=groups,dc=example,dc=com",
#    "is_staff": "cn=staff,ou=django,ou=groups,dc=example,dc=com",
#    "is_superuser": "cn=superuser,ou=django,ou=groups,dc=example,dc=com"
#}
#AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
#    "is_awesome": "cn=awesome,ou=django,ou=groups,dc=example,dc=com",
#}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

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
