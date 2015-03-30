"""
Local configuration files.

Please copy this file to "config.py", and change follow configurations.
"""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(CHANGE ME TO A LONG RANDOM STRING)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Set the time-zone based on the user's requirement
TIME_ZONE = 'Asia/Shanghai'
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Be carefully for SQLite. Since it doesn't support
# SELECT ... FOR UPDATE query, concurrency control of
# order status change will be disabled.
# Psycopg2 (PostgreSQL), Oracle, and MySQL database are known work well.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'store',
        'USER': 'username',
        'PASSWORD': 'password',
    }
}


# Change this under HTTP server.

STATIC_ROOT = '/srv/http/store/static/'

# Run follow commands to copy static files:
#   manage.py bower install
#   manage.py collectstatic
