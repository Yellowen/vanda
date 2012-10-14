# -----------------------------------------------------------------------------
#    Vanda Core - Vanda core utilities
#    Copyright (C) 2011 Sameer Rahmani <lxsameer@gnu.org>
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

# Unix client of websucks

import json
import _socket as socket


class UnixClient(object):
    """
    Unix client class.
    """
    def __init__(self, socket_address):
        self.sock = socket.socket(socket.AF_UNIX,
                                  socket.SOCK_STREAM)
        self.address = socket_address

    def send(self, msg, event="message", jsonize=True):
        data = msg
        try:
            self.sock.connect(self.address)

            if jsonize:
                data = json.dumps({"event": event, "data": json.dumps(msg)})
                data = "%s\r\n" % data
            else:
                data = "%s\r\n" % str(msg)
            self.sock.send(data)
        except socket.error, e:
            pass

        self.sock.close()
