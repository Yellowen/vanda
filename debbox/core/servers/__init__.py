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
import sys

from GEvent import GEventServer
from unixstream import UnixStream
from master import MasterServer, MasterClient


class WebServer (object):
    """
    Debbox internal web server main class.
    """

    def __init__(self, host, port, sslkey, sslcert,
                 settings, debug=False, interval=100000):

        self.host = host
        self.port = port
        self._key = sslkey
        self._cert = sslcert
        self.settings = settings
        self._debug = debug
        # since we don't use threads, internal checks are no more required
        sys.setcheckinterval = interval

    def start(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = self.settings

        server = GEventServer(self.host, self.port,
                              keyfile=self._key,
                              certfile=self._cert)

        if self._debug:
            from debbox.core.log import logger
            logger.info("Starting SSL connection with CERT:%s KEY: %s" % \
                        (self._cert, self._key))
            print 'Start SSL connection on ', (self.host, self.port)
        if self._debug:
            server.serve_forever()
        else:
            server.start()
