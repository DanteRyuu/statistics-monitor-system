import pika
import wmi

def getInfoCPU(c):
	usageCPU = 0
	for processor in c.Win32_Processor():
		no_processors = processor.NumberOfLogicalProcessors
		
	for process in c.InstancesOf('Win32_Process'):
		for p in c.Win32_PerfFormattedData_PerfProc_Process (IDProcess=process.ProcessID):
			processCPUusage = float(p.PercentProcessorTime)/no_processors
			if process.Caption == None:
				processorDesc = 'Unknown'
			else:
				processorDesc = process.Caption

			if processorDesc !='System Idle Process':
				processorUsageCPU = processCPUusage
				usageCPU += processorUsageCPU
				print ('Process ' + processorDesc + ', usage: ' + str(processorUsageCPU))
	usageCPU = '%.02f' % usageCPU
	
	return str(no_processors) + ';' + str(usageCPU)

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
	
def getInfoNetwork(c):
	netUsage = 0
	for net in c.Win32_PerfFormattedData_TCPIP_NetworkInterface():
		bytesTransfered = int(net.BytesTotalPerSec) * 8
		bandwidth = int(net.CurrentBandwidth)
		
		currentUsage = 0
		if bytesTransfered > 0:
			currentUsage = float(bytesTransfered*100)/bandwidth

		netUsage += currentUsage
		
	netUsage = '%.02f' % netUsage
	print 'Network usage: ' + netUsage
	return str(netUsage)

def getInfoDisk(c):
	for disk in c.Win32_PerfFormattedData_PerfDisk_PhysicalDisk(Name ='_Total'):
		diskUsage = disk.PercentDiskTime
		print 'Disk usage: ' + diskUsage + '%'
		
		return str(diskUsage)
	
def getInfo():
	c = wmi.WMI()
	message = ''
	for os in c.Win32_OperatingSystem():
		message += os.Caption
	message += ';' + getInfoCPU(c)
	message += ';' + getInfoMemory(c)
	message += ';' + getInfoNetwork(c)
	message += ';' + getInfoDisk(c)
	
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