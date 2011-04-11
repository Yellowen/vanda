from os import path


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
    }
}
# TODO: admin should select the pam service via an UI
PAM_SERVICE = "passwd"

ROOT_PATH = path.dirname(__file__)

# LOG options --------------------------------------------------------
# In this section you can change the logger options
# LOG_LEVEL specify the logger log level
CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
VERBOSE = 0  # log all levels
LOG_LEVEL = VERBOSE

# Define the format of log strings
#    %(name)s            Name of the logger (logging channel)
#    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
#                        WARNING, ERROR, CRITICAL)
#    %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
#                        "WARNING", "ERROR", "CRITICAL")
#    %(pathname)s        Full pathname of the source file where the logging
#                        call was issued (if available)
#    %(filename)s        Filename portion of pathname
#    %(module)s          Module (name portion of filename)
#    %(lineno)d          Source line number where the logging call was issued
#                        (if available)
#    %(funcName)s        Function name
#    %(created)f         Time when the LogRecord was created (time.time()
#                        return value)
#    %(asctime)s         Textual time when the LogRecord was created
#    %(msecs)d           Millisecond portion of the creation time
#    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
#                        relative to the time the logging module was loaded
#                        (typically at application startup time)
#    %(thread)d          Thread ID (if available)
#    %(threadName)s      Thread name (if available)
#    %(process)d         Process ID (if available)
#    %(message)s         The result of record.getMessage(), computed just as
#                        the record is emitted
LOG_FORMAT = '[%(asctime)s] [%(filename)s-%(funcName)s], \
line:%(lineno)d-> %(levelname)-8s : "%(message)s"'

# Define the date format that use in log strings
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_MAX_BYTES = 2 * 1024 * 1024  # 2Mb
LOG_BACKUP_COUNT = 5
LOG_FILENAME = path.join(ROOT_PATH, "../log/debbox")
LOG_FILENAME = "/var/log/debbox/webserver.log"


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
MEDIA_ROOT = path.join(ROOT_PATH, "../statics/").replace('\\', '/')
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
    path.join(ROOT_PATH, "templates").replace('\\', '/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
)


LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"
LOGIN_REDIRECT_URL = "/"
