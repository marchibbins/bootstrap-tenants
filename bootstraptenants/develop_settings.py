from settings import *

# Application definition
INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# http://stackoverflow.com/questions/20963856/improperlyconfigured-the-included-urlconf-project-urls-doesnt-have-any-patte
DEBUG_TOOLBAR_PATCH_SETTINGS = False

INTERNAL_IPS = (
    '127.0.0.1',
    '::1',
)

DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage'
