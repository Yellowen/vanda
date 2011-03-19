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

    def start(self):
        got_request_exception.connect(self.exception_printer)
        WSGIServer((self.host, self.port), WSGIHandler(),
                   **self.ssl).serve_forever()

    def exception_printer(self, sender, **kwargs):
        traceback.print_exc()
