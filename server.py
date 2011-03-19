#!/usr/bin/env python
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

# This modules runs fapws3 or gevent webserver and pass the requests to
# django wsgi handlers

import os
import sys

from optparse import OptionParser
from debbox.core.server import WebServer


parser = OptionParser()
parser.set_defaults(
    port='8000',
    backend='gevent',
    host='127.0.0.1',
    debug=True,
    settings='debbox.settings',
)

parser.add_option('--port', dest='port')
parser.add_option('--host', dest='host')
parser.add_option('--debug', dest='debug')
parser.add_option('--settings', dest='settings')
parser.add_option('--pythonpath', dest='pythonpath')


options, args = parser.parse_args()
if options.pythonpath:
    sys.path.insert(1, options.pythonpath)

sys.path.insert(1, "debbox/")

pid = os.fork()

if pid:
    # parent process
    pass
else:
    # child process

    # TODO: Get the ssl keys in the run time dynamically (fit to debian)
    __me__ = os.path.abspath(__file__)
    keyfile = os.path.join(os.path.dirname(__me__), 'ssl/server.key')
    certfile = os.path.join(os.path.dirname(__me__), 'ssl/server.crt')

    server = WebServer(options.host, int(options.port),
                       keyfile, certfile, options.settings,
                       options.debug)
    server.start()
