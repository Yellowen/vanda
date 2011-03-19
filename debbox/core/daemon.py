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

import os

from debbox.core.servers import WebServer


class DebboxDaemon (object):
    """
    Daemon class of debbox, this class runs the debbox
    as a deamon.
    """

    def __init__(self, options, config_dir="/etc/debbox/"):
        self.options = options
        self.pidfile = options.pidfile

    def _status(self):
        """
        checking for debbox processes.
        """
        if not os.path.exists(self.pidfile):
            return False

        self._masterpid, self._slavepid = file(self.pidfile).readlines()
        if os.path.exists("/proc/%s" % self._masterpid) and \
           os.path.exists("/proc/%s" % self._slavepid):
            return True

        else:
            os.unlink(self.pidfile)
            return False

    def start(self):
        """
        Start the Debbox server.
        """
        if self._status():
            print "Debbox is already running."
            return

        server = WebServer(self.options.host, int(self.options.port),
                           self.keyfile, self.certfile, self.options.settings,
                           self.ptions.debug)
        server.start()

    def stop(self):
        """
        Stop the debbox server.
        """
        if not self._status():
            print "Debbox is not running."
            return

    def status(self):
        """
        Return the status of debbox server.
        """
        if self._status():
            print "Debbox is running with Master: %s Slave: %s" % \
                  (self._masterpid, self._slavepid)
        else:
            print "Debbox is not running."

    def read_configs(self):
        """
        read the Debbox configuration files inside /etc/.
        """
        pass
