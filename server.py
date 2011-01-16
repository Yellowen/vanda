#!/usr/bin/env python
# This file is a part of fapws3 samples.
# all the hacks i made is under GPLv3 license
# i made some clean up in code that just moved some piece of code.

# This modules runs fapws3 webserver and pass the requests to
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
    host='127.0.0.1',
    # changed by lxsameer
    settings='src.settings',
)

parser.add_option('--port', dest='port')
parser.add_option('--host', dest='host')
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
