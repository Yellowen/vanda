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
import stat
import signal
import atexit
from pwd import getpwnam
from ConfigParser import ConfigParser
from ConfigParser import NoSectionError

from debbox.core.servers import WebServer
from debbox.core.communication import MasterServer
from debbox.core.servers import UnixStream
from debbox.core.logging.master import MasterLogger
from debbox.core.conf import SOCKFILE


class Debbox (object):
    """
    Daemon class of debbox, this class runs the Debbox in a daemon
    state (by default). You can think about this class as the main
    class of Debbox. This class use the *option* parameter for its
    configuration. *option* parameter is an object that created with
    optparser class and contains the command line parameters.

    if user decide to run the Debbox in background, then all of the
    IO transactions will redirect to given *stdin*, *stdout* and
    *stderr*.
    """

    def __init__(self, options, stdin='/dev/null', stdout='/dev/null',
                 stderr='/dev/null'):

        self.options = options

        # PID configurations ===================================
        self.piddir = options.piddir.rstrip("/")

        # debbox pid files
        self.mpid = "/".join((self.piddir, "debbox_master.pid"))
        self.spid = "/".join((self.piddir, "debbox_slave.pid"))

        # creating configuration object ========================
        #: confifgurewr
        self.config = ConfigParser()
        if os.path.exists(self.options.conf):
            self.config.read(self.options.conf)
        else:
            raise self.CantFindConfigFile()

        # reading SSL from config file
        self.ssl = {"key": self.config.get("SSL", "key"),
                    "cert": self.config.get("SSL", "cert"),
                    }

        # Setup ssl configuration for development environments
        root_tree = os.path.join(os.path.dirname(__file__),
                                 "../../")
        if self.ssl["key"] == "dev":
            self.ssl["key"] = os.path.join(root_tree, "ssl/server.key")

        if self.ssl["cert"] == "dev":
            self.ssl["cert"] = os.path.join(root_tree, "ssl/server.crt")

        # setting standard IO
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

        # Webserver should run under which user and group
        try:
            self.slave_user = self.config.get("User", "user", "debbox")
        except NoSectionError:
            print "Error: Can't find a suitable username in config file."
            sys.exit(1)

        try:
            self.slave_group = self.config.get("User", "group", "debbox")
        except NoSectionError:
            print "Error: Can't find a suitable group name in config file."
            sys.exit(1)

        # Setting up log directory
        self.logfolder = self.config.get("Log", "folder")
        if not os.path.exists(self.logfolder):
            try:
                os.makedirs(self.logfolder)
            except OSError, e:
                print e
                sys.exit(1)
        uid = getpwnam(self.slave_user)[2]
        gid = getpwnam(self.slave_user)[3]
        os.chown(self.logfolder, uid, gid)
        os.chmod(self.logfolder, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR | \
                 stat.S_IXGRP | stat.S_IWGRP | stat.S_IRGRP)

        self.logger = MasterLogger(self.config, "/".join((self.logfolder,
                                                  "master.log")),
                           self.options.debug)

        # Registering a cleanup method
        #atexit.register(self.__cleanup__)

    def __cleanup__(self):
        """
        Debbox destructor.
        """
        # removing servers pid files on exit
        if os.path.exists(self.mpid):
            try:
                os.remove(self.mpid)
            except OSError, e:
                self.logger.info("Error msg: %s" % e)
                raise

        if os.path.exists(self.spid):
            try:
                os.remove(self.spid)
            except OSError, e:
                self.logger.info("Error msg: %s" % e)
                raise

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
            try:
                os.remove(self.mpid)
            except OSError:
                pass
            try:
                os.remove(self.spid)
            except OSError:
                pass
            return False

    def start(self):
        """
        Start the Debbox server. all the daemon forking process runs here.
        """
        if self._status():
            print "Debbox is already running."
            return

        # Daemonizing Process ==============================
        # Please read about how a daemon work before asking
        # questions

        if not self.options.foreground:
            # First Fork
            pid = None
            try:
                pid = os.fork()
                self.logger.debug("First fork pid: %s" % pid)
            except OSError:
                raise self.CantFork("Can't create the master process.")

            if pid > 0:
                # Exist from parent
                self.logger.debug("First fork exit")
                sys.exit(0)

            os.umask(027)
            try:
                self._sid = os.setsid()
            except OSError:
                # TODO: check the exception
                raise

            # TODO: Where should we chdir? where is the safe place?

        self._masterpid = os.getpid()
        self.logger.debug("Master process at %s" % self._masterpid)

        # Second Fork =======================================
        slavepid = None
        try:
            slavepid = os.fork()
            self.logger.debug("Second fork pid: %s" % slavepid)
        except OSError:
            raise self.CantFork("Can't create the slave process")

        if slavepid > 0:

            # Master Process
            # Register the cleanup process.
            self._slavepid = slavepid
            signal.signal(signal.SIGUSR1, self._usr1_handler)
            if self.options.foreground:
                atexit.register(self.stop)

            # writing pid files
            if not self.options.foreground:
                file(self.mpid, "w+").write(str(self._masterpid))
                # TODO: find a way to build slave pid file in better time
                file(self.spid, "w+").write(str(slavepid))

            # running the master server
            socket = SOCKFILE
            masterapp = MasterServer(self.logger, self.config,
                                     self.options.debug)
            masterserver = UnixStream(socket, self.slave_user,
                                      masterapp.handler)
            print "Running Master Server . . ."
            if not self.options.debug or not self.options.foreground:
                self.io_redirect()
            if self.options.debug or self.options.foreground:
                masterserver.serve_forever()
            else:
                masterserver.start()

        else:
            # Slave process

            server = WebServer(self.options.host, int(self.options.port),
                               self.ssl["key"], self.ssl["cert"],
                               self.options.settings,
                               self.options.debug)

            uid = getpwnam(self.slave_user)[2]
            #gid = getpwnam(self.slave_user)[3]
            os.setuid(int(uid))
            #os.setgid(int(gid))
            os.umask(027)
            print "Running webserver on SSL connection at https://%s:%s/" % \
                  (self.options.host, self.options.port)
            if not self.options.debug or not self.options.foreground:
                self.io_redirect()
            self._slavepid = os.getpid()
            server.start()

    def stop(self):
        """
        Stop the debbox server, and clean the environment with
        removing any temporary files and pid files.
        """
        if not self.options.foreground:
            if not self._status():
                self.logger.info("Debbox is not running. . .")
                print "Debbox is not running. . ."
                return

            mpid = file(self.mpid).readlines()[0]
            spid = file(self.spid).readlines()[0]
            print "Stopping slave process."
            self.__cleanup__()
            os.kill(int(spid), 15)
            print "Stopping master process."
            os.kill(int(mpid), 15)

        sys.exit(0)

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
        """
        Redirect all the IO to given IOs in the constructor. and skip the
        redirecting process if daemon run in foreground ar debbug mode.
        """
        if not self.options.debug or not self.options.foreground:
            # Redirecting standard I/O to nowhere
            sys.stdout.flush()
            sys.stderr.flush()
            si = file(self.stdin, 'r')
            so = file(self.stdout, 'a+')
            se = file(self.stderr, 'a+', 0)
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

    def syncdb(self, dbname="default", fresh=False):
        """
        Try to sync the Django database by Debbox user. if ``fresh``
        argument was True, this method will recreate the database.
        """

        # First fork
        try:
            worker = os.fork()
        except OSError:
            raise self.CantFork("Can't create the slave process")

        if worker > 0:
            # Parent process
            self._slavepid = worker

            # Set SIGUSR1 handler
            signal.signal(signal.SIGUSR1, self._usr1_handler)

            # Set on exit handler
            if self.options.foreground:
                atexit.register(self.stop)

            # writing pid files
            if not self.options.foreground:
                file(self.mpid, "w+").write(str(os.getpid()))
                file(self.spid, "w+").write(str(worker))

            # running the master server
            socket = SOCKFILE
            masterapp = MasterServer(self.logger, self.config,
                                     self.options.debug)
            masterserver = UnixStream(socket, self.slave_user,
                                      masterapp.handler)

            print "Running Master Server . . ."
            masterserver.serve_forever()

        else:

            # Remove old database if we have to sync a fresh database
            if fresh:
                from debbox.settings import DATABASES
                print "Removing exist database . . ."
                try:
                    os.unlink(DATABASES[dbname]["NAME"])
                except OSError, e:
                    print "Warning: %s" % e
                    print "Skipping . . ."

            print "Syncing database . . ."
            uid = getpwnam(self.slave_user)[2]
            #gid = getpwnam(self.slave_user)[3]
            os.setuid(int(uid))
            #os.setgid(int(gid))
            os.umask(027)

            # Setting environment variables needed for django
            os.environ['DJANGO_SETTINGS_MODULE'] = self.options.settings

            # importing modules we need for our work after
            # preparing django
            from pysqlite2.dbapi2 import OperationalError

            from django.core.management import call_command
            from django.db.utils import DatabaseError

            from debbox.core.communication import MasterClient

            # Syncing give database
            try:
                call_command('syncdb', database=dbname)

            except OperationalError, e:
                print "Error: Unexpected error occured with '%s'"
                print "=================================================="
                print "Didn't you forget to create /var/lib/debbox/ and"
                print "change its ownership to Debbox defualt user ?"
                print "=================================================="

            except DatabaseError, e:
                print "Error: %s" % e
                print "Removing corrupted databases. . . "

                # Removing corrupted databases.
                from debbox.settings import DATABASES
                for db in DATABASES:
                    try:
                        os.unlink(DATABASES[db]["NAME"])
                    except OSError, e:
                        print "Warning: %s" % e
                        print "Skipping . . ."

                print "==================================================="
                print "You must sync the `default` database first."
                print "==================================================="

            # Send kill command to master server that cause terminating
            client = MasterClient()
            client.connect()
            client.command(command="kill")
            client.disconnect()

            return

    def _usr1_handler(self, signum, frame):
        """
        SIGUSR1 handler. debbox will treat SIGUSR1 just like SIGTERM.
        """

        #os.waitpid(self._slavepid, 0)
        if self.options.foreground:
            os.kill(self._slavepid, 15)
            mpid = os.getpid()
            os.kill(int(mpid), 15)
        self.stop()

    class CantFork (Exception):
        """
        This exception will raise if daemon can't for a new process.
        """
        pass

    class CantFindConfigFile (Exception):
        """
        This exception will raise if daemon can't find the Debbox
        main configuration file.
        """
        pass
