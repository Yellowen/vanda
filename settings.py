# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) 2010  Dina Project Community
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ---------------------------------------------------------------------------------


# Django settings for Dina project.
import os
import django



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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.devdb',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }





# FS_ROOT represent to the Dina root filesystem
FS_ROOT = os.path.dirname (__file__)

# APP_ROOT conatain the logic path to app dir
APP_ROOT = os.path.join (FS_ROOT , 'apps').replace ('\\' , '/')

# DINA_CACHE contain the path of a directory that all the cached data will live
DINA_CACHE = os.path.join (FS_ROOT , '.cache').replace ('\\' , '/')

# LOG options --------------------------------------------------------
# In this section you can change the logger options
# LOG_LEVEL specify the logger log level
#CRITICAL =50
#ERROR =40
#WARNING =30
#INFO =20
#DEBUG =10
#0 is for not set (log all levels)
LOG_LEVEL = 0

# Define the format of log strings
LOG_FORMAT = '[%(asctime)s] [%(name)s], line:%(lineno)d-> %(levelname)-8s : "%(message)s"'
# Define the date format that use in log strings
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
# Where to save logs
#LOG_FILE = FS_ROOT + "/dina.logs"
#Define the mode of log file. default is 'w'
#LOG_FILE_MODE = 'w'



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
MEDIA_ROOT = os.path.join (FS_ROOT , 'site_media').replace ('\\' , '/')


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
    # TODO: add a template loader for loading templates from a compress archive
    # TODO: add a template loader for loading templates from web
    'dina.fem.template.loaders.filesystem.load_template_source',
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware' ,
]




ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join (os.path.dirname (__file__) , 'templates').replace ('\\' ,'/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)







DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.comments',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.redirects',
]



DINA_APPS = [
    'dina.core',
    'dina.DPM',
    'dina.conf',
    'dina.fem.layout',
    'dina.utils.mptt',
    'dina.fem.menu',
    'dina.fem.page',
    'dina.auth',
    'dina.fem.layout',
    'apps.blog',
    'apps.contact',
    'apps.profile',
    'apps.addressbook',
    'apps.phonebook',
    'apps.projectmanagement',
]

INSTALLED_APPS = DJANGO_APPS[:] + DINA_APPS[:] 

# For working the contact send mail please complete flowing item
# add by pollesangi for contact
EMAIL_HOST = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = ''



# IMPORTANT: this code piece is just for debuging
# ----------------------------------------------------------------

if DEBUG : 
    import sys, os

    print "__name__ =", __name__
    print "__file__ =", __file__
    print "os.getpid() =", os.getpid()
    print "os.getcwd() =", os.getcwd()
    print "os.curdir =", os.curdir
    print "sys.path =", repr(sys.path)
    print "sys.modules.keys() =", repr(sys.modules.keys())
    print "sys.modules.has_key('dina-project') =", sys.modules.has_key('dina-project')
    
    if sys.modules.has_key('dina-project'):
        print "sys.modules['dina-project'].__name__ =", sys.modules['dina-project'].__name__
        print "sys.modules['dina-project'].__file__ =", sys.modules['dina-project'].__file__
        print "os.environ['DJANGO_SETTINGS_MODULE'] =", os.environ.get('DJANGO_SETTINGS_MODULE', None)

#---------------------------------------------------------------------



# INITIAL CODE ------------------------------------------------
if os.environ.get ('DJANGO_SETTINGS_MODULE', None) == None:
    # we have to export this environment variable to provide a init code .
    os.environ['DJANGO_SETTINGS_MODULE']  = 'settings'
    # this module import is just for initial code don't change it
    # and don't use it in your code
    from dina.log import Logger
    logger = Logger ('Settings')
    logger.info ("Initial code start point reached.")
    # IMPORTANT: check this section for other errors and better algorithm
    from django.db.utils import DatabaseError
    try:
        from dina import cache
        logger.info ("Initial code End point reached.")
    except DatabaseError:
        logger.critical ("It seems than your database does not exists.")
        logger.critical ("Please build your databse and syncdb it")
    

#--------------------------------------------------------------
