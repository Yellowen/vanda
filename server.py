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

# patching python standard threading
from gevent import monkey; monkey.patch_all()

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
    piddir="/var/run/",
    settings='debbox.settings',
)

parser.add_option('-k', dest='action',
                  help="Do ACTION on debbox. ACTION like {start|stop|status}")
parser.add_option('--shell', dest='shell',
                  action="store_true",
                  help="Execute a python shell (ipython), in the patched env.")
parser.add_option('-f', dest='foreground',
                  action="store_true",
                  help="Run Debbox on foreground.")
parser.add_option('-c', dest='conf',
                  help="Use CONF config file. default is" + \
                  "/etc/debbox/debbox.conf")
parser.add_option('--port', dest='port',
                  help="Run web server on PORT.")
parser.add_option('--host', dest='host',
                  help="Run web server on HOST.")
parser.add_option('--debug', dest='debug', action="store_true",
                  help="Activate debug mode.")
parser.add_option('--piddir', dest='piddir',
                  help="Stotr pid files in PIDDIR folder")
parser.add_option('--settings', dest='settings',
                  help="Django settings.py file")
parser.add_option('--syncdb', dest='sync', action="store_true",
                  help="Sync Debbox web application database.")
parser.add_option('--pythonpath', dest='pythonpath',
                  help="Add given path to python path.\n")

options, args = parser.parse_args()
valid_action = False

if options.pythonpath:
    sys.path.insert(1, options.pythonpath)
    
sys.path.insert(1, "debbox/")

try:
    daemon = Debbox(options)
except Debbox.CantFindConfigFile:
    print "Error: Can't find '%s' configuration file." % options.conf
    sys.exit(1)

if options.shell:
    from IPython.Shell import IPShellEmbed
    sys.argv = []
    ipshell = IPShellEmbed()
    ipshell()
    sys.exit(0)

# Try to syncdb
if options.sync:
    daemon.syncdb()
    valid_action = True

if options.foreground:
    daemon.start()

elif options.action == "start":
    daemon.start()

elif options.action == "stop":
    daemon.stop()

elif options.action == "status":
    daemon.status()

elif valid_action:
    sys.exit(0)

else:
    print "Error: what is '%s'" % options.action
    sys.exit(1)
