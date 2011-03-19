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
import sys
import atexit
from ConfigParser import ConfigParser

from debbox.core.servers import WebServer


class Debbox (object):
    """
    Daemon class of debbox, this class runs the debbox
    as a deamon.
    """

    def __init__(self, options, stdin='/dev/null', stdout='/dev/null',
                 stderr='/dev/null'):
        """
        Debbox constructor.
        """

        self.options = options
        self.pidfile = options.pidfile

        # creating configuration object
        self.config = ConfigParser()
        if os.path.exists(self.options.conf):
            self.config.read(self.options.conf)
        else:
            raise self.CantFindConfigFile()

        self.ssl = {"key": self.config.get("SSL", "key"),
                    "cert": self.config.get("SSL", "cert"),
                    }
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

        # Registering a cleanup method
        atexit.register(self.__cleanup__)

    def __cleanup__(self):
        """
        Debbox destructor.
        """
        if os.path.exist(self.pidfile):
            os.remove(self.pidfile)

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

        # Daemonizing Process ==============================
        # First Fork
        pid = None
        try:
            pid = os.fork()
            print ">>>> First fork pid: ", pid
        except OSError:
            raise self.CantFork("Can't create the master process.")

        if pid:
            # Exist from parent
            sys.exit(0)

        os.umask(027)
        try:
            self._sid = os.setsid()
        except OSError:
            # TODO: check the exception
            raise

        # TODO: Where should we chdir? where is the safe place?
        self.io_redirect()

        # Second Fork =======================================
        try:
            self._slavepid = os.fork()
        except OSError:
            raise self.CantFork("Can't create the slave process")

        if self._slavepid:
            # Master Process

        server = WebServer(self.options.host, int(self.options.port),
                           self.ssl["key"], self.ssl["cert"],
                           self.options.settings,
                           self.options.debug)
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

    def io_redirect(self):
        if not self.options.debug:
            # Redirecting standard I/O to nowhere
            sys.stdout.flush()
            sys.stderr.flush()
            si = file(self.stdin, 'r')
            so = file(self.stdout, 'a+')
            se = file(self.stderr, 'a+', 0)
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

    class CantFork (Exception):
        pass

    class CantFindConfigFile (Exception):
        pass
