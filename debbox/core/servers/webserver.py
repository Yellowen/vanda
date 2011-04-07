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
import time

#from GEvent import GEventServer
from django.core.handlers.wsgi import WSGIHandler
from master import MasterClient
from debbox.core.lotus import LotusDjango


class WebServer (object):
    """
    Debbox internal web server main class. based on gevent pywsgi server.

        .. py:attribute:: host

        Runs webserver on *host*.

        .. py:attribute:: port

        Bind webserver to given TCP *port*.

        .. py:attribute:: sskkey

        Path to the SSL key file.

        .. py:attribute:: sslcert

        Path to the SSL cert file.

        .. py:attribute:: settings

        Pythonic path to Django application settigns file.

        .. py:attribute:: debug

        Turn on the debugging mode.

        .. py:attribute:: interval

        Since we don't use threads, internal checks are no more required

        .. py:attribute:: statics_workers

        Number of workers for serving statics files.

    """

    def __init__(self, host, port, sslkey, sslcert,
                 settings, debug=False, interval=100000, statics_workers=1):

        self.host = host
        self.port = port
        self._key = sslkey
        self._cert = sslcert
        self.settings = settings
        self._debug = debug
        self._workers = statics_workers
        self.client = MasterClient()

        while True:
            try:
                self.client.connect()
                break
            except self.client.CantConnectToSocket:
                time.sleep(1)

        # since we don't use threads, internal checks are no more required
        sys.setcheckinterval = interval

    def start(self):
        """
        Start up webserver in blocking mode if debug mode is on and
        non-blocking mode if debug is off
        """

        os.environ['DJANGO_SETTINGS_MODULE'] = self.settings

        #server = GEventServer(self.host, self.port,
        #keyfile=self._key,
        #                      certfile=self._cert)
        server = LotusDjango(WSGIHandler(), self.host, self.port,
                            sslkey=self._key,
                            sslcert=self._cert,
                            debug=self._debug)

        if self._debug:
            from debbox.core.logging.instance import logger
            logger.info("Starting SSL connection with CERT:%s KEY: %s" % \
                        (self._cert, self._key))
            print 'Start SSL connection on ', (self.host, self.port)
        try:
            if self._debug:
                server.start()
            else:
                server.start()
        except:
            server.pool.stop()
            raise
