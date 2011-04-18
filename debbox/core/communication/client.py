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

# Communication Protocol specification ========================================
# Request:
# String format: JSON
# JSON data structure:
# {"command":  COMMAND,
#  "args" : {"arg1": value1, "arg2": value2, ....},
# }
#
# COMMAND: is the name of a function of method on the Master process
# args: will be a dict of arguments that should be passed to COMMAND function
#
# example:
# {"command": "echo",
#  "args": ["this is and example",]
# }
#
# Response:
# String format: JSON
# JSON data structure:
# {"status": STATUS,
#  "message": MSG,
#  "extra": EXTRA,
# }
#
# STATUS: is a integer value the will be 0 at success and !=0 un failed
# MSG: is a pickled data that return by Master COMMAND.
# EXTRA: is a extra flag, each command will use it for its own
# =============================================================================

import time
import pickle
import json
import _socket as socket


class MasterClient (object):
    """
    Client class for communicating with MasterServer.

    command method will send a command to MasterServer, use it like

       masterclient_instance.command(command='command_name',
                                     arg1='value', arg2=...)

    each argument that you provide for command method will pass to
    remote command, (Note: you should use arguments in keyword type
    not list type)

    command method will return an object that have three attribute
    status = return code of remote command, 0 means ok
    message = return result of remote command
    extra = extra flag of transport protocol

    also command exception will raise remote exception in MasterClient.
    """

    def __init__(self):
        import logging

        from debbox.core import conf
        self.socket = socket.socket(socket.AF_UNIX)

        logging.basicConfig(level=conf.LOG_LEVEL,
                            format=conf.LOG_FORMAT,
                            datefmt=conf.LOG_DATE_FORMAT)
        self.logger = logging.getLogger("MasterClient")

    def connect(self, wait_until_connect=False):
        """
        establish the connection to master socket.
        """
        from debbox.core.conf import SOCKFILE

        sockaddr = SOCKFILE

        if wait_until_connect:
            while True:
                try:
                    self.socket.connect(sockaddr)
                    self.logger.debug("Socket connection established.")
                    self.fd = self.socket.makefile("w+")
                    break

                except socket.error:
                    self.logger.debug("Can't connect to '%s'" % sockaddr + \
                                      " socket. Retry in 0.1 second.")
                    time.sleep(0.1)
        else:
            try:
                self.socket.connect(sockaddr)
                self.logger.debug("Socket connection established.")

                self.fd = self.socket.makefile("w+")
            except socket.error:
                self.logger.error("Can't connect to '%s' socket" % sockaddr)
                raise self.CantConnectToSocket()

    def command(self, command=None, **kwargs):
        """
        send a command to master process.
        """
        if not command:
            raise self.EmptyCommand()
        packet = {"command": command,
                  "args": kwargs}

        jpacket = "%s\n" % json.dumps(packet)
        self.fd.write(jpacket)
        self.fd.flush()

        self.logger.debug("Data sent: %s" % jpacket)
        buf = self.fd.readline()
        buf = json.loads(buf)
        self.logger.debug("Data Received: %s" % buf)

        # raising remote exception
        # TODO: transport remote traceback somehow
        if buf["extra"] == "debug":
            try:
                exception = pickle.loads(str(buf["message"]))
                self.logger.warning("Remote exception raised exception: %s" % \
                                    exception)

                raise exception

            except TypeError:
                self.logger.warning("Can't unpickle the remote exception.")
                raise self.UnpicklableException(buf['string'])
        # creating a result object
        result = type("Result", (object,),
                      {"status": buf["status"],
                       "result": pickle.loads(str(buf["message"])),
                       "extra": buf["extra"]})

        return result()

    def disconnect(self):
        """
        disconnect the master socket.
        """
        self.fd.close()
        self.logger.debug("Disconnecting")
        self.socket.close()

    class CantFindConfigFile (Exception):
        pass

    class CantConnectToSocket (Exception):
        pass

    class EmptyCommand (Exception):
        pass

    class UnpicklableException (Exception):
        pass
