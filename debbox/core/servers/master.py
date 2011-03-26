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

# Transport protocol specification ============================================
# Request:
# String format: JSON
# JSON data structure:
# {"command":  COMMAND,
#  "args" : {"arg1": value1, "arg2": value2, ....],
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


import os
import sys
import pickle
import json
import _socket as socket
from ConfigParser import ConfigParser, NoSectionError
#from debbox.core.log import logger

from debbox.core.auth.pam import pam


class MasterServer (object):
    """
    Master process application class.
    """

    def __init__(self, logger_instance, debug=False):
        self.logger = logger_instance
        self.debug = debug
        # TODO: make command dictionary loadable form a file
        self.commands = {
            "echo": self.echo,
            "authenticate": pam.authenticate,
            }

    def _dumpmsg(self, status, msg, extra=None):
        """
        return a json form data message to transport via socket
        """
        return "%s\n" % json.dumps({"status": status,
                           "message": pickle.dumps(msg),
                           "extra": extra})

    def handler(self, socket, address):
        """
        Unix stream server handler, this method will receive all
        the data from unix socket.

        address is an emtry variable.
        """
        # using a makefile because we want to use readline()
        fileobj = socket.makefile()

        # main loop of master process
        # all the received data will proccess here
        while True:

            # read a line from socket
            line = fileobj.readline()
            if not line:
                # client disconnected
                self.logger.info("Client disconnected")
                break

            try:
                # try to restruct json data
                data = json.loads(line)

            except ValueError:
                # data format is invalid
                fileobj.write(self._dumpmsg(-1, "invalid format"))
                continue

            if "command" in data:
                command = data["command"]
                args = {}
                if "args" in data:
                    args = data["args"]
                print "Receive Command: %s, args: %s" % (command, str(args))
                if command in self.commands:
                    try:
                        result = self.commands[command](**args)
                        fileobj.write(self._dumpmsg(0, result))
                        fileobj.flush()
                        continue

                    except:
                        if self.debug:
                            fileobj.write(self._dumpmsg(-1,
                                                sys.exc_info()[1],
                                                extra="debug"))
                            fileobj.flush()
                            continue
                        else:
                            fileobj.write(self._dumpmsg(-1,
                                                        "An error occured"))
                            fileobj.flush()
                            continue

                else:
                    fileobj.write(self._dumpmsg(-1, "command not found"))
                    fileobj.flush()
                    continue
            else:
                fileobj.write(self._dumpmsg(-1, "malform command"))
                fileobj.flush()
                continue

    def echo(self, **kwargs):
        """
        this is a echo command. just for testing.
        """
        return kwargs


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
        # getting the config file address by reading the tmp file
        # in /tmp/debbox_<parent pid>
        parentpid = os.getppid()
        filename = "/tmp/debbox_%s" % parentpid
        try:
            config_address = file(filename).readline()
        except IOError:
            # TODO: handle this IOError
            #logger.error("Can't find the temporary file.")
            print "IOERROR"
            raise

        # Reading config file
        self.config = ConfigParser()
        if os.path.exists(config_address):
            self.config.read(config_address)
        else:
            raise self.CantFindConfigFile()

        # creating the socket object and connecting that to master
        # socket
        self.socket = socket.socket(socket.AF_UNIX)

    def connect(self):
        """
        establish the connection to master socket.
        """
        sockaddr = "/tmp/debbox.sock"
        try:
            sockaddr = self.config.get("Socket", "master",
                                                "/tmp/debbox.sock")
        except NoSectionError:
            pass

        try:
            self.socket.connect(sockaddr)
            #logger.debug("Socket connection established.")
            print "Connection established"
            self.fd = self.socket.makefile("w+")
        except socket.error:
            #logger.error("Can't connect to '%s' socket" % sockaddr)
            print "Can't connect"
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
        print "Data sent: %s" % jpacket
        buf = self.fd.readline()
        buf = json.loads(buf)

        # raising remote exception
        # TODO: transport remote traceback somehow
        if buf["extra"] == "debug":
            exception = pickle.loads(str(buf["message"]))
            print exception
            raise exception

        # creating a result object
        result = type("Result", (object,),
                      {"status": buf["status"],
                       "result": pickle.loads(str(buf["message"])),
                       "extra": buf["extra"]})

        print "Data Received: %s" % buf
        return result()

    def disconnect(self):
        """
        disconnect the master socket.
        """
        self.fd.close()
        print "Disconnecting"
        self.socket.close()

    class CantFindConfigFile (Exception):
        pass

    class CantConnectToSocket (Exception):
        pass

    class EmptyCommand (Exception):
        pass
