import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='stats_queue', durable=True)
print ' '

def callback(ch, method, properties, body):
    info = body.split(';')
    print ('OS: ' + info[0])
    print ('CPU: ' + info[1] + '%')
    print ('Total RAM: ' + info[2])
    print ('Free RAM: ' + info[3])
	
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='stats_queue')

channel.start_consuming()