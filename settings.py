# Django settings for Dina_CMS project.
import os



#+++ Remember to shut down the debug mode in official release
#@@@ for more information about $$something$$ string take a look at doc/devel/coding.policy
DEBUG = True
TEMPLATE_DEBUG = DEBUG



ADMINS = (
  
    #+++ this section should filled with installer system
    ('$$ADMIN_NAME$$' , '$$ADMIN_MAIL$$'),
    # example
    # ('Your Name', 'your_email@domain.com'),
)





MANAGERS = ADMINS



#--- Database configuration -------------------------------------------------------------------------------------------
#@@@ we use sqlite3 for ower development but in the official release this section will fill with installer

if DEBUG:
    # don't change this section
    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = 'db.devdb'
else:

    DATABASE_ENGINE = '$$DB_ENGINE$$'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = '$$DB_NAME$$'             # Or path to database file if using sqlite3.
    DATABASE_USER = '$$DB_USER$$'             # Not used with sqlite3.
    DATABASE_PASSWORD = '$$DB_PASSWD$$'         # Not used with sqlite3.
    DATABASE_HOST = '$$DB_HOST$$'             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = '$$DB_PORT$$'             # Set to empty string for default. Not used with sqlite3.

#-----------------------------------------------------------------------------------------------------------------------

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$3%mti-%a0$)-h3x-ak_92s&o2p8j96r&kwbbjv&w936@1b9#d'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

# original one
#ROOT_URLCONF = 'Dina_CMS.urls'
#ower changed one
ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join (os.path.dirname (__file__) , 'templates').replace ('\\' .'/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)



#@@@ Never use never use the dir name Dina_CMS in module starts
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
)
