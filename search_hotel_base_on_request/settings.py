from __future__ import absolute_import
# ^^^ The above is required if you want to import from the celery
# library.  If you don't have this then `from celery.schedules import`
# becomes `proj.celery.schedules` in Python 2.x since it allows
# for relative imports by default.

# Celery settings

BROKER_URL = 'amqp://guest:guest@localhost//'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
#CELERY_TIMEZONE = 'Asia/Ho_Chi_Minh'

#CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
#CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',


CELERYBEAT_SCHEDULER =  'djcelery.schedulers.DatabaseScheduler'


#from celery.schedules import crontab


#args = {'from_date': datetime.now() + timedelta(days=1),
#        'to_date'  : datetime.now() + timedelta(days=3)
#        }

#CELERYBEAT_SCHEDULE = {
#    'craw_agoda_every_day': {
#        'task': 'celery_app.tasks.crawl_spider1',
#        'schedule': crontab(hour=15, minute=15),
##        'schedule': timedelta(minutes=2),
#        'args': ('agoda.com',1, 13)
#    },
#
#    'craw_ivivu_every_day': {
#        'task': 'celery_app.tasks.crawl_spider',
#        'schedule': crontab(hour=11, minute=22),
##        'schedule': timedelta(minutes=2),
#        'args': ('ivivu.com',1, 13)
#    },
#}



"""
Django settings for search_hotel_base_on_request project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vw*9#p8@woph*)-%1t^-(jq25*wk3hb5uu_agfg9195!+91a7r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hotel',
    'south',
    'djcelery',
    'celery_app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'search_hotel_base_on_request.urls'

WSGI_APPLICATION = 'search_hotel_base_on_request.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'hotel_demo',                      # Or path to database file if using sqlite3.
        'USER': 'openerp',                      # Not used with sqlite3.
        'PASSWORD': 'openerp',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#Define template path
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'hotel/templates')]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

GRAPPELLI_ADMIN_TITLE = 'Admin Panel - Search Hotel Base On Request'
