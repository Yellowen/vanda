# -----------------------------------------------------------------------------
#    WebSucks - WebSocket server for Vanda Platform
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

import pika


class AMQServer(object):

    def __init__(self, host, socket, port=None, virtual_host=None,
                 user=None, password=None, frame_max=None,
                 channel_max=None, heartbeat=None):
        self.connection = None
        self.channel = None
        self.host = host
        self.params = {"host": host}
        if port:
            self.params["port"] = port
        if virtual_host:
            self.params["virtual_host"] = virtual_host
        if user and password:
            credentials = pika.PlainCredentials(user, password)
            self.params["credentials"] = credentials

        if frame_max:
            self.params["frame_max"] = frame_max
        if channel_max:
            self.params["channel_max"] = channel_max
        if heartbeat:
            self.params["heartbeat"] = heartbeat
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

        parameters = pika.ConnectionParameters(**self.params)
        self.connection = pika.SelectConnection(parameters,
                                                self.on_connected)
        print "AMQServer started . . . "
        try:
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            self.connection.close()
            self.connection.ioloop.start()
