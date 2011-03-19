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

import sys

from optparse import OptionParser

from debbox.core.daemon import Debbox


parser = OptionParser()
parser.set_defaults(
    port='8000',
    backend='gevent',
    host='127.0.0.1',
    debug=False,
    conf="/etc/debbox/debbox.conf",
    pidfile="/var/run/",
    settings='debbox.settings',
)

parser.add_option('-k', dest='action')
parser.add_option('--port', dest='port')
parser.add_option('-c', dest='conf')
parser.add_option('--host', dest='host')
parser.add_option('--debug', dest='debug')
parser.add_option('--piddir', dest='piddir')
parser.add_option('--settings', dest='settings')
parser.add_option('--pythonpath', dest='pythonpath')

options, args = parser.parse_args()

if options.pythonpath:
    sys.path.insert(1, options.pythonpath)


sys.path.insert(1, "debbox/")

try:
    daemon = Debbox(options)
except Debbox.CantFindConfigFile:
    print "Error: Can't find '%s' configuration file." % options.conf
    sys.exit(1)

if options.action == "start":
    daemon.start()

elif options.action == "stop":
    daemon.stop()

elif options.action == "status":
    daemon.status()

else:
    print "Error: what is '%s'" % options.action
    sys.exit(1)
