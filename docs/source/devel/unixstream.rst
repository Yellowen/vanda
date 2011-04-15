Unix Stream Server
******************
.. py:currentmodule:: debbox.core.servers

:py:class:`UnixStream` class is a streaming server over the unix domain socket, that create a unix socket and wait for connection. It will pass all the 
incoming connections to its handler that usually is a external application or code.

Unix Stream Class
=================
.. autoclass:: debbox.core.servers.UnixStream
   :members:
