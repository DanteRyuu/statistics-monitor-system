import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='stats_queue', durable=True) #durable, so that RabbitMQ
														 #doesn't lose the queue

channel.basic_publish(exchange='',
                      routing_key='stats_queue',
                      body="Hello World!",
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # persistent messages
                      ))
print (" [x] Sent %r" % (message,))
connection.close()