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
                                        backlog=self.backlog)
            self.address = self.socket.getsockname()
            print "UNIXSTREAM>>>> ", self.address
        self._stopped_event.clear()

    def start_accepting(self):
        if self._accept_event is None:
            self._accept_event = self.loop.io(self.socket.fileno(), 1)
            self._accept_event.start(self._do_accept)

    def _start_accepting_if_started(self, _event=None):
        if self.started:
            self.start_accepting()

    def stop_accepting(self):
        if self._accept_event is not None:
            self._accept_event.stop()
            self._accept_event = None
        if self._start_accepting_timer is not None:
            self._start_accepting_timer.stop()
            self._start_accepting_timer = None

    def _do_accept(self, event, _evtype):
        assert event is self._accept_event
        address = None
        try:
            if self.full():
                self.stop_accepting()
                return
            try:
                client_socket, address = self.socket.accept()
            except socket.error, err:
                if err[0] == errno.EAGAIN:
                    return
                raise
            self.delay = self.min_delay
            client_socket = socket.socket(_sock=client_socket)
            spawn = self._spawn
            if spawn is None:
                self._handle(client_socket, address)
            else:
                spawn(self._handle, client_socket, address)
            return
        except:
            traceback.print_exc()
            ex = sys.exc_info()[1]
            if self.is_fatal_error(ex):
                self.kill()
                sys.stderr.write('ERROR: %s failed with %s\n' % (self, str(ex) or repr(ex)))
                return
        try:
            if address is None:
                sys.stderr.write('%s: Failed.\n' % (self, ))
            else:
                sys.stderr.write('%s: Failed to handle request from %s\n' % (self, address, ))
        except Exception:
            traceback.print_exc()
        if self.delay >= 0:
            self.stop_accepting()
            self._start_accepting_timer = self.loop.timer(self.delay)
            self._start_accepting_timer.start(self._start_accepting_if_started)
            self.delay = min(self.max_delay, self.delay * 2)

    def is_fatal_error(self, ex):
        return isinstance(ex, socket.error) and ex[0] in (errno.EBADF, errno.EINVAL, errno.ENOTSOCK)

    def wrap_socket_and_handle(self, client_socket, address):
        # used in case of ssl sockets
        ssl_socket = self.wrap_socket(client_socket, **self.ssl_args)
        return self.handle(ssl_socket, address)

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

    def kill(self):
        """
        Close the listener socket and stop accepting.
        """
        self.started = False
        try:
            self.stop_accepting()
        finally:
            try:
                self.socket.close()
            except Exception:
                pass
            self.__dict__.pop('socket', None)
            self.__dict__.pop('handle', None)

    def stop(self, timeout=None):
        """
        Stop accepting the connections and close the listening socket.

        If the server uses a pool to spawn the requests, then `stop` also waits
        for all the handlers to exit. If there are still handlers executing
        after *timeout*  has expired (default 1 second), then the currently
        running handlers in the pool are killed.
        """
        self.kill()
        if timeout is None:
            timeout = self.stop_timeout
        if self.pool:
            self.pool.join(timeout=timeout)
            self.pool.kill(block=True, timeout=1)
        self.post_stop()

    def post_stop(self):
        self._stopped_event.set()

    def serve_forever(self, stop_timeout=None):
        """
        Start the server if it hasn't been already started and wait until
        it's stopped.
        """
        # add test that serve_forever exists on stop()
        if not self.started:
            self.start()
        try:
            self._stopped_event.wait()
        except:
            self.stop(timeout=stop_timeout)
            raise


def _unix_listener(address, backlog=10):
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


def test_app(socket, address):
    print 'New connection from %s:%s' % address
    # using a makefile because we want to use readline()
    fileobj = socket.makefile()
    fileobj.write('Welcome to the echo server! Type quit to exit.\r\n')
    fileobj.flush()
    while True:
        line = fileobj.readline()
        if not line:
            print "client disconnected"
            break
        if line.strip().lower() == 'quit':
            print "client quit"
            break
        fileobj.write(line)
        fileobj.flush()
        print "echoed", repr(line)
