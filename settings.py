# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) $YEAR$  $AUTHOR$
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


# FS_ROOT represent to the Dina root filesystem
FS_ROOT = os.path.dirname (__file__)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join (FS_ROOT , 'site_media').replace ('\\' , '/')

# APP_ROOT conatain the logic path to app dir
APP_ROOT = os.path.join (FS_ROOT , 'apps').replace ('\\' , '/')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'


DPM_CACHE = os.path.join (FS_ROOT , 'cache').replace ('\\' , '/')

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$3%mti-%a0$)-h3x-ak_92s&o2p8j96r&kwbbjv&w936@1b9#d'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    # TODO: add a template loader for loading templates from a compress archive
    # TODO: add a template loader for loading templates from web
    'dina.template.loaders.filesystem.load_template_source',
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

]




# original one
#ROOT_URLCONF = 'Dina_Project.urls'
#ower changed one
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
]



DINA_APPS = [
    'dina.core',
    'dina.DPM',
    'dina.conf',
    'dina.utils.mptt',
    'dina.fem.menu',
    'dina.fem.page',
    'apps.blog',  
]

INSTALLED_APPS = DJANGO_APPS[:] + DINA_APPS[:] 

