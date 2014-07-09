from settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
# http://stackoverflow.com/questions/20963856/improperlyconfigured-the-included-urlconf-project-urls-doesnt-have-any-patte
DEBUG_TOOLBAR_PATCH_SETTINGS = False 

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
    'debug_toolbar',
    'inspector_panel',
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'inspector_panel.panels.inspector.InspectorPanel',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bstenants',
        'USER': 'bstenants',
        'PASSWORD': 'bstenants',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Email
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'