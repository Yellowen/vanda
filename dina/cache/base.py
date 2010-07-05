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

import os

from django.conf import settings

class NoCacheModuleName (Exception):
    pass


class CacheObject (object):
    """
    Base class for cache classes, this class take care of
    some IO transactions.
    """
    def __init__ (self, cache_module_name=None):
        super(CacheObject, self).__init__ ()
        if cache_module_name is None:
            raise NoCacheModuleName ("No cache module name specified.")
        self._cache_dir = "%s/%s" % (settings.DINA_CACHE , cache_module_name)
        

    def _check_for_cache_dir (self):
        """
        Check for exists cache dir. if cache dir does not exits
        it will create the cache dir.
        """
        if not os.path.exist (self._cache_dir):
            # TODO: Here we should deal with OSError [Error 13]: permission denied
            # exception .
            os.mkdir (self._cache_dir)
        return

    
    
        

