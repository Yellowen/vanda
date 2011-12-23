# -----------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011 Some Hackers In Town
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
# -----------------------------------------------------------------------------

LOADING = False


def typediscover():
    """
    automatically walk throught the project and import data types of
    ultra_blog.
    """
    import sys

    global LOADING

    if LOADING:
        return
    LOADING = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        try:
            __import__(app)
            app_path = sys.modules[app].__path__
        except AttributeError:
            continue
        try:
            imp.find_module('types', app_path)
        except ImportError:
            continue
        __import__("%s.types" % app)
        #app_path = sys.modules["%s.types" % app]
    LOADING = False
