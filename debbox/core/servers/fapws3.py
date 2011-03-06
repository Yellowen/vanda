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


from fapws import base
import fapws._evwsgi as evwsgi
from fapws.contrib import django_handler, views


class FAPWSServer (object):
    """
    FAPWS server class.
    """

    def __init__(self, host, port):
        print "asdasdasD"
        self.host = host
        self.port = port

    def start(self):
        evwsgi.start(self.host, self.port)
        evwsgi.set_base_module(base)
        evwsgi.wsgi_cb(('', self.generic))
        evwsgi.set_debug(0)
        evwsgi.run()

    def generic(self, environ, start_response):
        res = django_handler.handler(environ, start_response)
        return [res]
