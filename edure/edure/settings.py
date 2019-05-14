# Django settings for edure project.
import os
import getpass
import djcelery
djcelery.setup_loader()


DEBUG = True

TEMPLATE_DEBUG = DEBUG
PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

FILESIZELIMIT = 1048576 * 5
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
MANAGERS = ADMINS
ADMIN_PHONE = ''
ADMIN_EMAIL = 'wetech@wetechgroups.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'edure',
        'USER': 'edure',
        'PASSWORD': 'edure',
        'HOST': 'localhost',
        'PORT': '',
    }
}

#if getpass.getuser() == 'ubuntu':
#    DATABASES = {
#        'default': {
#            'ENGINE': 'django.db.backends.postgresql_psycopg2',
#            'NAME': 'edure',
#            'USER': 'eduredb',
#            'PASSWORD': 'eduredb123',
#            'HOST': 'eduredb.cphomzcpukck.us-east-1.rds.amazonaws.com',
#            'PORT': '5432',
#        }
#    }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*', 'ec2-52-20-229-140.compute-1.amazonaws.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Jakarta'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
CSRF_COOKIE_DOMAIN = 'ec2-52-20-229-140.compute-1.amazonaws.com'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# CAPTCHA SETTINGS
CAPTCHA_FONT_PATH = os.path.join(PROJECT_PATH, 'courier.ttf')
CAPTCHA_FONT_SIZE = 34

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    #'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#rj!&#1rml6u81l!lm8w1$u_321(e1gd88i!51irap(b_omv8k'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
     #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'edure.middleware.DefaultMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'responsive.middleware.DeviceInfoMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LOGIN_URL = '/'
ROOT_URLCONF = 'edure.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'responsive.context_processors.device_info'
)

DEFAULT_BREAKPOINTS = {
    'phone': 480,
    'tablet': 767,
    'desktop': None,
}

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'edure.wsgi.application'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'voidsolutiondev@gmail.com'
EMAIL_HOST_PASSWORD = 'testertester'
DEFAULT_FROM_EMAIL = 'Edure <support@edure.in>'

# compression setup
#COMPRESS_ENABLED = True
#COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']
#COMPRESS_URL = MEDIA_URL
#COMPRESS_ROOT = MEDIA_ROOT
#COMPRESS_PARSER = 'compressor.parser.LxmlParser'

DJANGO_WYSIWYG_FLAVOR = "tinymce_advanced"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
USER_AGENTS_CACHE = 'default'


INSTALLED_APPS = (
    'djcelery',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'django_wysiwyg',
    'tinymce',
    #'compressor',
    'django_user_agents',
    'paypal.standard.ipn',
    'rest_framework',
    'edure',
    'captcha',
    'djorm_pgfulltext',
    'responsive',
    'easy_thumbnails',
    'import_export',
    'service',

    # Static Files will be saved to AmazonS3
    'django_s3_storage',

    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = os.path.join(PROJECT_PATH, 'media') + '/edure-81e107c05989.json'
GOOGLE_PICKER_SECRET = 'BF1X-FWg1Pd7YUWOkAc-Oz2a'
DROPBOX_ACCESS_TOKEN = 'VXUUvpdXomAAAAAAAAABO4JqI4MLQzsgYfBI4fALI78uOV219NU5WjYXplM2JmBg'
DROPBOX_CONSUMER_KEY = 'o3lodpdhmr43anj'
#DROPBOX_CONSUMER_SECRET = 'o3lodpdhmr43anj'


THUMBNAIL_ALIASES = {
    '': {
        'foto': {'size': (100, 100), 'crop': True},
    },
}

PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = 'hadi@tokowebku.com'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_PATH, 'log/edure.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'request_handler': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(PROJECT_PATH, 'log/edure.log'),
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'standard',
        },
    },
    'loggers': {

        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
