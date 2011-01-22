# -----------------------------------------------------------------------------
#    Debbox - Modern administration panel for Debian GNU/Linux
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

import os
from core.log import logger


class BaseParser (object):
    """
    Base class for all type of config parser.
    """

    def __init__(self, inputfile, cached=True):
        self._file = inputfile
        self.cached = cached
        self._dict = {}
        if os.path.exists(self._file) and cached:
            self._buf = self._read()
            # parse the string to config
            self.__config__()
        else:
            self._buf = None
        self.load()

    def _read(self):
        return self._file.read()

    def load(self):
        pass

    def get_option(self, option_name, default_value=None):
        if option_name in self._dict.keys():
            return self._dict[option_name]
        else:
            return default_value

    def __getitem__(self, key):
        if key in self._dict:
            return self._dict[key]
        else:
            raise self.KeyError(key)

    def set_option(self, option_name, option_value):
        self._dict[option_name] = option_value

    def __setitem__(self, key, value):
        self._dict[key] = value

    def commit(self):
        """
        write configuration into file.
        """
        if self._buf:
            try:
                fd = open(self._file, "w")
                fd.write(self.__unicode__)
            except:
                raise

    def __config__(self):
        """
        This method parse the self._buf string to a dictionary. and should
        override by any inherited class.
        """
        pass

    def __unicode__(self):
        """
        BaseParser use this standard method to convert self._buf to
        real confiuration string. This method should override by user.
        """
        pass

    class KeyError (Exception):
        pass

    class TypeNotSupported (Exception):
        pass


class Parser (object):
    pass
