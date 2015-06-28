import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='stats_queue', durable=True)
print (' [*] Waiting for messages.')

def callback(ch, method, properties, body):
    print (" [x] Received %r" % (body,))
	
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='stats_queue')

channel.start_consuming()