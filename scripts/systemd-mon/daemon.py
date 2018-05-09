#!/usr/bin/env python
import sys
import subprocess
import psutil
import getopt

# Parse arguments #
def set_args():
    minimal = False
    cfgfile = "service.ini"
    counter = 1
    if len(sys.argv) > 1:
    	try:
    	    opts, args = getopt.getopt(sys.argv[1:], 'mc:', ['minimal=', 'config='])
    	except getopt.GetoptError:
    	    sys.exit(2)
    	for opt, arg in opts:
    		if opt in ('-m', '--minimal'):
    	            minimal = True
    		if opt in ('-c', '--config'):
    	            cfgfile = str(arg)
                    counter += 1
    return minimal, cfgfile
# Read the service from a file. The file name, as well as every service name must be correct and on a seperate line. Error handling is not supported yet. #
def load_service(service, cfg):
    file = open(cfg, "r")
    for line in file:
    	service.append(line)
     return service

# Check information for services #

def check_info():
    # Initialize variables #
    service = []
    minim = False
    minim, cfg = set_args()
    service = load_service(service, cfg)
    isActive = []
    taskNum = {}
    counter = 0
    mainPID = {}
    mainProc = ""
    childProcHandle = []
    childProcPID = []
    childProcName = []
    childProcCPU = []
    childProcMemory = []
    childProcStatus = []
    mainProcConnections = []
    serviceNumActive = ''
    serviceNumFailed = ''
    serviceTotal = ''

    # A cycle to get all the information from console output we need into variables #

    serviceTotal = str(subprocess.check_output("systemctl list-units --all | grep 'loaded units listed'", shell=True))
    serviceTotal = serviceTotal[2:-24]
    serviceTotal = serviceTotal.strip()
    serviceTotal = [int(number) for number in serviceTotal.split() if number.isdigit()]
    serviceTotal = int(''.join(map(str, serviceTotal)))
    serviceNumActive = str(subprocess.check_output("systemctl list-units --type service | grep 'loaded units listed'", shell=True))
    serviceNumActive = serviceNumActive[2:-74]
    serviceNumActive = serviceNumActive.strip()
    serviceNumActive = [int(number) for number in serviceNumActive.split() if number.isdigit()] # read numeric value
    serviceNumActive = int(''.join(map(str, serviceNumActive))) # convert to int
    serviceNumFailed = str(subprocess.check_output("systemctl --failed | grep 'loaded units listed'", shell=True)) #doing the same
    serviceNumFailed = serviceNumFailed[2:-74]
    serviceNumFailed = serviceNumFailed.strip()
    serviceNumFailed = [int(number) for number in serviceNumFailed.split() if number.isdigit()]
    serviceNumFailed = int(''.join(map(str, serviceNumFailed)))
    print("Number of total loaded units: {}".format(serviceTotal))
    print("Number of active units: {}".format(serviceNumActive))
    print("Number of failed units: {}".format(serviceNumFailed))
    print('')

    if minim == False:
    	for line in service:
    		service[counter] = service[counter].strip() # strip extra new lines #
    		isActive.append(int(subprocess.check_output("systemctl status %s | grep -c 'active (running)'" % service[counter], shell=True))) 
    		taskNum[service[counter]] = str(subprocess.check_output("systemctl status %s | grep 'Tasks: '" % service[counter], shell=True))
    		mainPID[service[counter]] = str(subprocess.check_output("systemctl status %s | grep 'Main PID: '" % service[counter], shell=True)) 

    		# Formatting the strings to ensure they are human-readable #

    		taskNum[service[counter]] = taskNum[service[counter]].lower()
    		taskNum[service[counter]] = taskNum[service[counter]].strip()
    		taskNum[service[counter]] = taskNum[service[counter]][:-3]
    		taskNum[service[counter]] = taskNum[service[counter]][6:]

    		mainPID[service[counter]] = mainPID[service[counter]].strip()
    		mainPID[service[counter]] = [int(number) for number in mainPID[service[counter]].split() if number.isdigit()] # read the numeric value of PID
    		mainPID[service[counter]] = int(''.join(map(str, mainPID[service[counter]]))) # converting the mainPID to integer, so we can use it in psutil


    		# Getting process information #

    		mainProcHandle = psutil.Process(mainPID[service[counter]])
    		mainProc = mainProcHandle.name()
		mainProcStatus = mainProcHandle.status()
    		mainProcMem = mainProcHandle.memory_percent()
    		mainProcCPU = mainProcHandle.cpu_percent(interval=1.0)

    		# Reserved for future updates to include child process information, but need to work on that #

        #       mainProcConnections = mainProcHandle.connections()
	#       childProcHandle = mainProcHandle.children()
	#       for child in childProcHandle:
	#	childProcPID[child] = int(childProcHandle[child].pid)
	#   	childProcName[child] = str(childProcHandle[child].name())
	#   	childProcStatus[child] = childProcHandle[child].status()
	#   	childProcCPU[child] = childProcHandle[child].cpu_percent(interval=1.0)
	#   	childProcMemory[child] = childProcHandle[child].memory_percent()

    		# Print all the information we need #

    		if isActive[counter] >= 1:
    		        print("Service: %s" % service[counter])
    			print("Status: active and running.")
    			print("Running %s" % taskNum[service[counter]])
    			print("Main PID of service: %s" % mainPID[service[counter]])
    			print("Name of main process: %s" % mainProc)
    			print("Main process status: %s" % mainProcStatus)
    			print("Main process CPU usage(percent): %f" % mainProcCPU)
    			print("Main process RAM usage(percent): %f" % mainProcMem)
    #			print("Main process net connections: %s" % mainProcConnections)
    #			for ch in childProcHandle:
    #			print("Child process name: %s" % childProcName[ch])
    #			print("Child process ID: %d" % childProcPID[ch])
    #			print("Child process status: %s" % childProcStatus[ch])
    #			print("Child process CPU usage: %f" % childProcCPU[ch])
    #			print("Child process memory usage: %f" % childProcMemory[ch])
    			print("")

    		else:
    			print("%s is inactive or an error has occured" % service[counter])
                counter += 1




check_info()


