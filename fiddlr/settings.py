"""
Django settings for fiddlr project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


gmaps_api_key = 'AIzaSyCnOiybCXuruO3EII8NV1aEsa7SWE6mrJg'

# Automatically detect whether this is running on my development
# computer, otherwise assuming that the environment is production.
isProduction = False
#isProduction = True
try:
    open('.devmachine')
except IOError:
    isProduction = True




from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i=8luhlg5bs9%*p1z-1jlumcixyv5*8k**6^1vc(*n&+ns-4hf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not isProduction
TEMPLATE_DEBUG = not isProduction
#DEBUG = True
#TEMPLATE_DEBUG = True


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJNU5YCE2AUPUHVKQ' #for ted
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'fiddlr'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_HEADERS = {
#    'x-amz-acl': 'public-read',
}



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'home',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fiddlr.urls'

WSGI_APPLICATION = 'fiddlr.wsgi.application'



REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 50,
}




ADMINS = (
    ('lol Theodore', 'tplorts@gmail.com'),
)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'fiddlr.backend@gmail.com'
EMAIL_HOST_PASSWORD = 'discoball'
EMAIL_PORT = 587


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True



###################
# HEROKU SETTINGS #

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(),
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
S3_STATIC_URL = 'https://fiddlr.s3.amazonaws.com/'
if isProduction:
    STATIC_URL = S3_STATIC_URL
else:
    STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
