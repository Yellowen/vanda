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


class MQServer(object):

    def __init__(self, host, socket):
        self.connection = None
        self.channel = None
        self.host = host
        self.socket = socket

    def on_closed(self, frame):
        # connection.ioloop is blocking, this will stop and exit the app
        self.connection.ioloop.stop()

    def on_connected(self, connection):
            self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel_):
        self.channel = channel_
        self.channel.queue_declare(queue="test", durable=True,
                                   exclusive=False, auto_delete=False,
                                   callback=self.on_queue_declared)

    def on_queue_declared(self, frame):
        self.channel.basic_consume(self.handle_delivery,
                                   queue='test')

        # Add a callback so we can stop the ioloop
        self.connection.add_on_close_callback(self.on_closed)

    def handle_delivery(self, channel, method_frame, header_frame, body):
        print "RECV: ", body
        self.socket.send(body)
        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def run(self):
        parameters = pika.ConnectionParameters(self.host)
        self.connection = pika.SelectConnection(parameters,
                                                self.on_connected)
        print "Server started . . . "
        self.connection.ioloop.start()


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
