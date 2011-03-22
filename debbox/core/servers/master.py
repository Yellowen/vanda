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

import json


class Master (object):
    """
    Master process application class.
    """

    def __init__(self, logger_instance):
        self.logger = logger_instance

    def _dumpmsg(self, status, msg):
        return json.dumps({"status": status,
                           "message": msg})

    def handler(self, socket, address):
        """
        Unix stream server handler, this method will receive all
        the data from unix socket.

        address is an emtry variable.
        """
        # using a makefile because we want to use readline()
        fileobj = socket.makefile()
        while True:
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
            
