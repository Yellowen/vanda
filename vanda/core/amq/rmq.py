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

# RabbitMQ implementation

# This file contain the interfaces for communication with RabbitMQ

import pika
import json

from django.conf import settings


class RMQBlockingInterface(object):

    def get_option(self, option_name, default=None):
        if hasattr(settings, option_name):
            return getattr(settings, option_name)
        else:
            return default

    def __init__(self):

        host = self.get_option("AMQ_HOST", 'localhost')
        port = self.get_option("AMQ_PORT")
        virtual_host = self.get_option("AMQ_VH")
        user = self.get_option("AMQ_USERNAME")
        password = self.get_option("AMQ_PASSWORD")
        frame_max = self.get_option("AMQ_FM")
        channel_max = self.get_option("AMQ_CM")
        heartbeat = self.get_option("AMQ_HEARTBEAT")

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

    def send(self, queue, msg):
        parameters = pika.ConnectionParameters(**self.params)
        connection = pika.BlockingConnection(parameters)

        # Open the channel
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue=queue, durable=True,
                              exclusive=False, auto_delete=False)

        # Construct a message and send it
        channel.basic_publish(exchange='',
                              routing_key=queue,
                              body=json.dumps(msg),
                              properties=pika.BasicProperties(
                                  content_type="text/plain",
                                  delivery_mode=1))
