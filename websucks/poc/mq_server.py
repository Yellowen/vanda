import pika


class MQServer(object):

    def __init__(self, host):
        self.connection = None
        self.channel = None
        self.host = host

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
        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def run(self):
        parameters = pika.ConnectionParameters(self.host)
        self.connection = pika.SelectConnection(parameters,
                                                self.on_connected)
        print "Server started . . . "
        self.connection.ioloop.start()


server = MQServer('localhost')
server.run()
