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

from django.core.signals import got_request_exception

from base import LotusServer


class LotusDjango (LotusServer):
    """
    Lotus Specific Django web server.
    """

    def __init__(self, WSGI_app, host, port,
                 sslkey, sslcert, debug=True):

        got_request_exception.connect(self.exception_printer)

        from debbox.core.logging.instance import logger
        self.logger = logger

        super(LotusDjango, self).__init__(WSGI_app, host, port,
                                          sslkey, sslcert, debug=True)

    def exception_printer(self, sender, **kwargs):
        import sys

        tblist = traceback.extract_tb(sys.exc_info()[2])
        strlist = traceback.format_list(tblist)
        log = "Uncaught Exception occur:\n" + "".join(strlist)
        self.logger.critical(log)
