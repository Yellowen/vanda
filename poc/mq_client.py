import pika
import json

# Create our connection parameters and connect to RabbitMQ
parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(parameters)

# Open the channel
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue="test", durable=True,
                  exclusive=False, auto_delete=False)

# Construct a message and send it
channel.basic_publish(exchange='',
                  routing_key="test",
                  body=json.dumps({"asdasd": "Asdasd"}),
                  properties=pika.BasicProperties(
                      content_type="text/plain",
                      delivery_mode=1))

