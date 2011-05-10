import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# TODO: replace the database address in the deb installation
# time.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "/var/lib/debbox/debbox.db",
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'vpkg': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "/var/lib/debbox/vpkg.db",
    },
}


DATABASE_ROUTERS = ['vpkg.routers.VPKGRouter']

# TODO: admin should select the pam service via an UI
PAM_SERVICE = "passwd"

ROOT_PATH = os.path.dirname(__file__)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Tehran'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# IMPORTANT: current MEDIA_ROOT value is only for development
MEDIA_ROOT = os.path.join(ROOT_PATH, "../statics").replace("\\", "/")
STATIC_ROOT = MEDIA_ROOT
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/statics/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'h+%nw-dyh8wey!&sps$rh(o(%lwx!-c@bilu(mn+$kp_ffrkiw'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

AUTHENTICATION_BACKENDS = (
    'core.auth.pam.backend.PAMAuthentication',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'debbox.urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, "templates").replace('\\', '/'),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'vpkg',
]


LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"
LOGIN_REDIRECT_URL = "/"

if 'DEBBOX_SYNCDB' in os.environ:
    if os.environ['DEBBOX_SYNCDB'] != "vpkg":

        # do not involve vpkg if syncing database was vpkg
        from debbox.core.logging import logger
        from vpkg.discover import ApplicationDiscovery

        discovery = ApplicationDiscovery(logger=logger)
        INSTALLED_APPS.extend(discovery.installed_applications())
        logger.info(INSTALLED_APPS)
    del os.environ['DEBBOX_SYNCDB']
