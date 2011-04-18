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


from json import dumps, loads

from core.log import logger
from core.confparser.parser import BaseParser

# CN : Please be described Method class
class JSONConfParser (BaseParser):
    """
    Generic json type configuration parser.
    """
    def __config__(self):
        if self._buf:
            try:
                self._dict = loads(self._buf)
            except:
                raise self.TypeNotSupported
        else:
            return None

    def __unicode__(self):
            return dumps(self._dict)

    @classmethod
    def is_suitable(cls, buf):
        if buf:
            try:
                loads(buf)
                return cls

            except Exception, e:
                logger.debug("JSONConfParser > %s > TypeNotSupported" % e)
                return None
        else:
            return None
