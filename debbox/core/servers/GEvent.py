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


import traceback

from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer

from django.core.handlers.wsgi import WSGIHandler
from django.core.signals import got_request_exception


class GEventServer (object):
    """
    GEvent server backend class.
    """
    def __init__(self, host, port, **ssl):
        self.host = host
        self.port = port
        self.ssl = ssl
        got_request_exception.connect(self.exception_printer)
        from debbox.core.logging import logger
        logger.debug(">> SSL: %s" % self.ssl)
        self.server = WSGIServer((self.host, self.port), WSGIHandler(),
                   **self.ssl)

    def start(self):
        self.server.start()

    def serve_forever(self):
        self.server.serve_forever()

    def exception_printer(self, sender, **kwargs):
        import sys
        from debbox.core.logging import logger

        tblist = traceback.extract_tb(sys.exc_info()[2])
        strlist = traceback.format_list(tblist)
        log = "Uncaught Exception occur:\n" + "".join(strlist)
        logger.critical(log)
