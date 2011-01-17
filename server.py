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

# I borrow some lines from fapws3 and gevent samples.

# This modules runs fapws3 or gevent webserver and pass the requests to
# django wsgi handlers

import os
import sys
import time
from optparse import OptionParser

import django
from fapws import base
import fapws._evwsgi as evwsgi
from fapws.contrib import django_handler, views

parser = OptionParser()
parser.set_defaults(
    port='8000',
    backend='gevent',
    host='127.0.0.1',
    settings='src.settings',
)

parser.add_option('--port', dest='port')
parser.add_option('--host', dest='host')
parser.add_option('--backend', dest='backend')
parser.add_option('--settings', dest='settings')
parser.add_option('--pythonpath', dest='pythonpath')


options, args = parser.parse_args()


os.environ['DJANGO_SETTINGS_MODULE'] = options.settings

# since we don't use threads, internal checks are no more required
sys.setcheckinterval = 100000 

if options.pythonpath:
    sys.path.insert(1, options.pythonpath)

print 'start on', (options.host, options.port)
evwsgi.start(options.host, options.port)
evwsgi.set_base_module(base)


def generic(environ, start_response):
    res=django_handler.handler(environ, start_response)
    return [res]

evwsgi.wsgi_cb(('', generic))
evwsgi.set_debug(0)
evwsgi.run()
