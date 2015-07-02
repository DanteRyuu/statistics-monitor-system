# statistics-monitor-system

Helpful links:
	-https://technodesk.wordpress.com/2009/09/25/python-monitor-process-cpu-using-wmi/
	-http://www.blog.pythonlibrary.org/2010/10/03/how-to-find-and-list-all-running-processes-with-python/
	-http://www.mahmoudthoughts.com/2011/01/get-network-utilization-using-vbs.html
	
MSDN -> Win32 classes:
	-OperatingSystem: https://msdn.microsoft.com/en-us/library/aa394239%28v=vs.85%29.aspx
	-Process: https://msdn.microsoft.com/en-us/library/aa394372%28v=vs.85%29.aspx
	-PerfRawData_PerfProc_Process: https://msdn.microsoft.com/en-us/library/aa394323%28v=vs.85%29.aspx
	-PerfFormattedData_PerfProc_Process: https://msdn.microsoft.com/en-us/library/aa394277%28v=vs.85%29.aspx
	-PerfFormattedData_Tcpip_NetworkInterface: https://msdn.microsoft.com/en-us/library/aa394293%28v=vs.85%29.aspx
	-PerfFormattedData_PerfDisk_PhysicalDisk: https://msdn.microsoft.com/en-us/library/aa394262%28v=vs.85%29.aspx
	-ComputerSystemProduct: https://msdn.microsoft.com/en-us/library/aa394105%28v=vs.85%29.aspx
	
To do:
	- using threads to gather info faster
	- linux agent
	- use a database for storing info
	- unit-test the app
	- find a unique id for machines --- done
	- gather additional info
	- set default/specified timers for sending periodic updates