import copy

import pika
import gevent
from gevent.coros import Semaphore as Lock
from gevent.queue import Queue

from ws4py.exc import StreamClosed
from ws4py.server.handler.threadedhandler import WebSocketHandler as \
     ThreadedHandler
from ws4py.server.geventserver import WebSocketServer
from ws4py.server.wsgi.middleware import WebSocketUpgradeMiddleware




class WebSocketHandler(ThreadedHandler):
    """
    WebSocket API for handlers
    This provides a socket-like interface similar to the browser
    WebSocket API for managing a WebSocket connection.
    """

    def __init__(self, sock, protocols, extensions, environ):
        ThreadedHandler.__init__(self, sock, protocols, extensions)

        self.environ = environ

        self._messages = Queue()
        self._lock = Lock()
        self._th = gevent.spawn(self._receive)

    def closed(self, code, reason=None):
        self._messages.put(StreamClosed(code, reason))

    def received_message(self, m):
        self._messages.put(copy.deepcopy(m))

    def receive(self, msg_obj=False):
        msg = self._messages.get()

        if isinstance(msg, StreamClosed):
            # Maybe we'll do something better
            return None

        if msg_obj:
            return msg
        else:
            return msg.data


class WSServer(WebSocketServer):

    def __init__(self, *args, **kwargs):
        gevent.pywsgi.WSGIServer.__init__(self, *args, **kwargs)
        protocols = kwargs.pop('websocket_protocols', [])
        extensions = kwargs.pop('websocket_extensions', [])
        self.application = WebSocketUpgradeMiddleware(
            self.application,
            protocols=protocols,
            extensions=extensions,
            websocket_class=WebSocketHandler,
            )


def echo_handler(websocket, environ):
    try:
        ## while True:

        ##     msg = websocket.receive(msg_obj=True)

        ##     pprint(websocket.__dict__)

        ##     if msg is not None:
        ##         websocket.send(msg.data, msg.is_binary)
        ##     else:
        ##         break
        server = MQServer('localhost', websocket)
        server.run()

    finally:
        print "<<< close"
        websocket.close()

print "Server start on localhost:9000"
server = WSServer(('127.0.0.1', 9000), echo_handler)
server.serve_forever()
