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
from pwd import getpwnam  
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
        self.piddir = options.piddir.rstrip("/")

        # debbox pid files
        self.mpid = "/".join((self.piddir, "debbox_master.pid"))
        self.spid = "/".join((self.piddir, "debbox_slave.pid"))

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

        # Webserver should run under which user and group
        self.slave_user = self.config.get("User", "user", "debbox")
        self.slave_group = self.config.get("User", "group", "debbox")

        # Registering a cleanup method
        atexit.register(self.__cleanup__)

    def __cleanup__(self):
        """
        Debbox destructor.
        """
        if os.path.exist(self.mpid):
            os.remove(self.mpid)

        if os.path.exist(self.spid):
            os.remove(self.spid)

    def _status(self):
        """
        checking for debbox processes.
        """
        if not os.path.exists(self.mpid):
            return False
        if not os.path.exists(self.spid):
            return False

        self._masterpid = file(self.mpid).readlines()[0]
        self._slavepid = file(self.spid).readlines()[0]
        if os.path.exists("/proc/%s" % self._masterpid) and \
           os.path.exists("/proc/%s" % self._slavepid):
            return True

        else:
            os.unlink(self.mpid)
            os.unlink(self.mpid)
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
        self._masterpid = os.getpid()

        # Second Fork =======================================
        slavepid = None
        try:
            slavepid = os.fork()
        except OSError:
            raise self.CantFork("Can't create the slave process")

        if slavepid:
            # Master Process
            print "here in Master"
            if self.options.debug:
                os.waitpid(slavepid, 0)
        else:
            # Slave process
            os.setuid()
            uid = getpwnam(self.slave_user)[2]
            # TODO: should we use slave_user for gid too?
            gid = getpwnam(self.slave_group)[3]
            os.setuid(uid)
            os.setgid(gid)
            os.umask(027)
            self.io_redirect()
            self._slavepid = os.getpid()
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
        if os.path.exists(self.mpid):
            print "Debbox Master process is running with '%s' pid" % \
                  file(self.mpid).readlines()[0]
        else:
            print "Debbox Master is not running."

        if os.path.exists(self.spid):
            print "Debbox Slave process is running with '%s' pid" % \
                  file(self.spid).readlines()[0]
        else:
            print "Debbox Slave is not running."

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
