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

import sys
import pickle
import json
from ConfigParser import NoOptionError

from debbox.core.commands import MASTER_COMMANDS


class MasterServer (object):
    """
    Master process application class.
    """

    def __init__(self, logger_instance, config, debug=False):
        self.logger = logger_instance
        self.debug = debug
        self.config = config
        # TODO: make command dictionary loadable form a file
        self.commands = {
            "echo": self.echo,
            "get_config": self.get_config,
            "kill": self.kill,
            }
        [MASTER_COMMANDS.pop(i) for i in \
         MASTER_COMMANDS if i in self.commands.keys()]
        self.commands.update(MASTER_COMMANDS)

    def _dumpmsg(self, status, msg, extra=None):
        """
        return a json form data message to transport via socket
        """
        packet = {"status": status,
                  "message": pickle.dumps(msg),
                  "extra": extra}

        if extra:
            packet["string"] = str(msg)

        return "%s\n" % json.dumps(packet)

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
                self.logger.debug("Receive Command: %s, args: %s" % \
                                  (command, str(args)))
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
                    self.logger.error("Command not found.")
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

    def get_config(self, config):
        """
        return the requested config entry.

           .. py:attribute: config

              A tuple that contains the config section key as the first element
              and entry name as the second element.

        """
        default = None
        result = None
        if len(config) > 2:
            default = config[2]
        try:
            result = self.config.get(config[0], config[1], default)
        except NoOptionError, e:
            raise Exception(e)
        return result

    def kill(self):
        """
        kill the master process by sending a SIGUSR1 to debbox daemon.
        """
        import os
        import signal
        os.kill(os.getpid(), signal.SIGUSR1)
