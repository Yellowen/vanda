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
import pickle
import json


# Transport protocol specification ============================================
# Request:
# String format: JSON
# JSON data structure:
# {"command":  COMMAND,
#  "args" : [arg1, arg2, ....],
# }
#
# COMMAND: is the name of a function of method on the Master process
# args: will be a list of arguments that should be passed to COMMAND function
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


class Master (object):
    """
    Master process application class.
    """

    # TODO: make command dictionary loadable form a file
    commands = {
        "echo": self.echo,
        }

    def __init__(self, logger_instance, debug=False):
        self.logger = logger_instance
        self.debug = debug

    def _dumpmsg(self, status, msg, extra=None):
        """
        return a json form data message to transport via socket
        """
        return json.dumps({"status": status,
                           "message": msg,
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
                if command in self.commands:
                    try:
                        result = self.commands[command](**args)
                    except:
                        if self.debug:
                            fileobj.write(self._dumpmsg(-1, pickle.dumps(-1,
                                                                sys.exc_info(),
                                                                extra="debug")
                                                        ))
                            continue
                        else:
                            pass
                else:
                    fileobj.write(self._dumpmsg(-1, "command not found"))
                    continue
            else:
                fileobj.write(self._dumpmsg(-1, "malform command"))
                continue
