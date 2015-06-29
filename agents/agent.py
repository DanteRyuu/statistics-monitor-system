import pika
import wmi

def getInfoCPU(c):
	usageCPU = 0
	for process in c.InstancesOf('Win32_Process'):
		for p in c.Win32_PerfRawData_PerfProc_Process (IDProcess=process.ProcessID):
			currentCPUtime, currentTimestamp = long(p.PercentProcessorTime), long(p.Timestamp_Sys100NS)
			if process.Caption == None:
				processorDesc = 'Unknown'
			else:
				processorDesc = process.Caption
			try:
				processorUsageCPU = (float(currentCPUtime)/float(currentTimestamp)*100)
			except ZeroDivisionError:
				processorUsageCPU = 0

			usageCPU += processorUsageCPU
			print ('Process ' + processorDesc + ', usage: ' + str(processorUsageCPU))
	usageCPU = '%.04f' % usageCPU
	
	return str(usageCPU)

def getInfoMemory(c):
	for os in c.Win32_OperatingSystem():
		physicalMemory = float(os.TotalVisibleMemorySize)
		print 'Total memory: ' + str(physicalMemory) + ' KiB'
		freeMemory = float(os.FreePhysicalMemory)
		print 'Free memory: ' + str(freeMemory) + ' KiB'
		unit = ' KiB'
		
		while physicalMemory / 1024 > 1 or unit == ' TiB':
			physicalMemory = physicalMemory / 1024
			
			if freeMemory / 1024 >= 1:
				freeMemory = freeMemory / 1024

			if unit == ' KiB':
				unit = ' MiB'
			elif unit == ' MiB':
				unit = ' GiB'
			else:
				unit = ' TiB'
		
		physicalMemory = '%.02f' % physicalMemory
		freeMemory = '%.02f' % freeMemory
		
		return str(physicalMemory) + unit + ';' + str(freeMemory) + unit
	
def getInfoNetwork():
	pass
	
def getInfo():
	c = wmi.WMI()
	message = ''
	for os in c.Win32_OperatingSystem():
		message += os.Caption
	message += ';' + getInfoCPU(c)
	message += ';' + getInfoMemory(c)
	
	return message

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='stats_queue', durable=True) #durable, so that RabbitMQ
														 #doesn't lose the queue

channel.basic_publish(exchange='',
                      routing_key='stats_queue',
                      body=getInfo(),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # persistent messages
                      ))

connection.close()