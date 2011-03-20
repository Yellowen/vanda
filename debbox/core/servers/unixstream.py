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

import _socket

from gevent.baseserver import BaseServer


class UnixStream(BaseServer):
    """
    A unix socket stream server. this server will be run as the Master
    process in debbox
    """

    def set_listener(self, listener, backlog=None):
        if not isinstance(listener, str):
            raise TypeError('Expected a unix address: %r' % listener)

        if backlog is not None:
            self.backlog = backlog

        self.address = listener

    @property
    def server_host(self):
        """
        Address that the server is bound to (string).
        """
        return self.address

    def pre_start(self):
        """
        If the user initialized the server with an address rather than socket,
        then this function will create a socket, bind it and put it
        into listening mode.

        It is not supposed to be called by the user, it is called by
        `start` before starting the accept loop.
        """

        if not hasattr(self, 'socket'):
            self.socket = _unix_listener(self.address,
                                        backlog=self.backlog,
                                        reuse_addr=self.reuse_addr)
            self.address = self.socket.getsockname()
        self._stopped_event.clear()

    def start(self):
        """
        Start accepting the connections.
        If an address was provided in the constructor, then also create
        a socket, bind it and put it into the listening mode.
        """

        assert not self.started, '%s already started' % self.__class__.__name__
        self.pre_start()
        self.started = True
        try:
            self.start_accepting()
        except:
            self.kill()
            raise


def _unix_listener(address, backlog=50, reuse_addr=None):
    """
    A shortcut to create a unix socket, bind it and put it into listening
    state.
    """
    sock = _socket.socket(_socket.AF_UNIX)
    sock.bind(address)
    sock.listen(backlog)
    # 0 means non-blocking and 1 means blocking
    # blocking:
    # any recv or send call wait until finishing their process
    # non-blocking:
    # if recv or send or any communication function can't reach their resource
    # or can't do their job an exception will raise

    # TODO: does non-blocking is good for our goal
    sock.setblocking(0)
    return sock
