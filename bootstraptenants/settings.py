"""
Django settings for bootstraptenants project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ID = os.environ.get('SITE_ID', 1)
SITE_SECURE = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', False))
TEMPLATE_DEBUG = bool(os.environ.get('TEMPLATE_DEBUG', False))

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'index',
    'password_reset',
    'bootstrapform',
    'avatar',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'index.context_processors.site',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'index.middleware.SetLastVisitMiddleware',
)

ROOT_URLCONF = 'bootstraptenants.urls'
WSGI_APPLICATION = 'bootstraptenants.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {
    'default': dj_database_url.config()
}

# Auth
AUTH_USER_MODEL = 'index.CustomUser'
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

CSRF_FAILURE_VIEW = 'index.views.error403'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'

# # AWS and S3
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', False)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', False)
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', False)
# S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', False)

# Avatar
AVATAR_HASH_FILENAMES = True
AVATAR_HASH_USERDIRNAMES = True
AVATAR_MAX_AVATARS_PER_USER = 1
AVATAR_GRAVATAR_BACKUP = False
AVATAR_DEFAULT_URL = 'images/tenants.jpg'
AVATAR_DEFAULT_STAFF_URL = 'images/staff.jpg'
AVATAR_AUTO_GENERATE_SIZES = (30, 125,)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOST', '*')
]

# Email
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)
EMAIL_USE_TLS = bool(os.environ.get('EMAIL_USE_TLS', False))

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

# Admins
ADMINS = (
    ('Marc Hibbins', 'marchibbins@gmail.com'),
    ('Gareth Foote', 'gareth.foote@gmail.com'),
)
MANAGERS = ADMINS

# Location IP addresses
LOCATION_IPS = (
    '127.0.0.1',
)

APPEND_SLASH = False

BUILDING_IMAGES = (
    'colourworks',
    'fitzroyhouse',
    'printhouse',
)