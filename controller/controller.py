import pika
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
engine = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Stats(Base):
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    os = Column(String)
    no_processors = Column(Integer)
    cpu = Column(Float)
    memory = Column(String)
    free_memory = Column(String)
    network = Column(Float)
    disk = Column(Float)

    def __repr__(self):
       return "<Stats(UUID='%s', OS='%s', Processors='%s', CPU='%s'%, Total RAM='%s', Free RAM='%s', Network usage='%s'%, DiskI/O='%s'%)>" % (
                           self.uuid, self.os, self.no_processors, self.cpu, self.memory, self.free_memory, self.network, self.disk)

Stats.__table__ 
Table('stats', MetaData(bind=None),
            Column('id', Integer(), table=<stats>, primary_key=True, nullable=False),
            Column('uuid', String(), table=<stats>),
            Column('os', String(), table=<stats>),
            Column('no_processors', Integer(), table=<stats>),
            Column('cpu', Float(), table=<stats>),
            Column('memory', String(), table=<stats>),
            Column('free_memory', String(), table=<stats>),
            Column('network', Float(), table=<stats>),
            Column('disk', Float(), table=<stats>), schema=None)

Base.metadata.create_all(engine) 

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='stats_queue', durable=True)
print ' '

def callback(ch, method, properties, body):
	info = body.split(';')
	print ('UUID: ' + info[0])
	print ('OS: ' + info[1])
	print ('Processors: ' + info[2])
	print ('CPU: ' + info[3] + '%')
	print ('Total RAM: ' + info[4])
	print ('Free RAM: ' + info[5])
	print ('Network usage: ' + info[6] + '%')
	print ('Disk I/O: ' + info[7] + '%')

	ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='stats_queue')

channel.start_consuming()