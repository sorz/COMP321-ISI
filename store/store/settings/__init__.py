"""
Django settings for store project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6#n380hklnpdtav+@242dw0mrj5bq#*6s-g88en1-d6pny(w)%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'sorl.thumbnail',
    'djangobower',
    'bootstrap3',
    'store',
    'product',
    'category',
    'cart',
    'order',
    'account',
    'admin',
    'category_admin',
    'product_admin',
    'account_admin',
    'order_admin'
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

ROOT_URLCONF = 'store.urls'

WSGI_APPLICATION = 'store.wsgi.application'

LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'
LOGIN_REDIRECT_URL = '/account/profile/'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# SQLite is only used for testing, and
# concurrency control of order status change will be disabled.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),

    # Make PyCharm recognize bower's static files.
    # In production, it should be commented out before "manage.py collectstatic".
    os.path.join(BASE_DIR, "bower/bower_components"),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "djangobower.finders.BowerFinder"
)


# Django-bower
# https://django-bower.readthedocs.org/en/latest/installation.html

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, "bower")

BOWER_INSTALLED_APPS = (
    'jquery#1.11',
    'jquery.cookie',
    'bootstrap',
    'bootstrap-datepicker',
)


# Where to store uploaded files. Make sure it's writable.
# e.g /var/media

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Make IDE happy.
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'store', 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request"
)


# Loading local settings.
try:
    from .config import *
except ImportError:
    print("Warning: local configuration not found.", file=sys.stderr)
    print("Please see store/settings/config.sample.py for detail.", file=sys.stderr)
