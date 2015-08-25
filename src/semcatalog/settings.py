"""
Django settings for semcatalog project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from semcatalog.local import SECRET_KEY

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PRODUCTION_HOST_NAME = 'crd-software.lbl.gov'

# gets FQDN to determine production server
import socket
if socket.getfqdn() == PRODUCTION_HOST_NAME:
    PRODUCTION = True
    BASE_LOG = '/var/log/django'
else:
    PRODUCTION = False
    BASE_LOG = BASE_DIR

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '' # from local config file

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'semcatalog.urls'

WSGI_APPLICATION = 'semcatalog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# URLs
STATIC_URL = '/media/'
MEDIA_URL = STATIC_URL + 'media/'
if PRODUCTION:
    MEDIA_ROOT = os.path.join(BASE_DIR, os.pardir, os.pardir, os.pardir, 'html', 'media', 'media')
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static') + '/',)

# email
DEFAULT_FROM_EMAIL = "no-reply@crd-software.lbl.gov"
EMAIL_SUBJECT_PREFIX = '[CRD-Software]'
if PRODUCTION:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = False
    EMAIL_HOST = 'smtp.lbl.gov'
    EMAIL_PORT = '25'
#     EMAIL_HOST_USER -- defined in protected password file / or not defined (no authentication)
#     EMAIL_HOST_PASSWORD -- defined in protected password file / or not defined (no authentication)
else:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = '/Users/gilberto/Documents/dev/ameriflux_svn/ameriflux/python/fit/static/email'
