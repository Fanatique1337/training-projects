#!/usr/bin/env python

# Import needed libraries

import sys, subprocess, psutil, getopt
sys.tracebacklimit = 4
#########################################

# Parse the arguments

def set_args():
	minimal = False
	cfgfile = "services.conf"
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

# Read the services from a given file (either by default or by the config argument) # Service names must be on seperate line

def load_service(service, cfg):
	file = open(cfg, "r")
	for line in file:
		service.append(line)
	file.close()
	return service

# Gather information for the services

def check_info():

	# Initializing variables

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
	childProcCPU = []
	childProcMemory = []
	totalProcCPU = 0.0
	totalProcMem = 0.0
	serviceNumActive = ''
	serviceNumFailed = ''
	serviceTotal = ''

	# A cycle to get all the information needed for the daemons into our variables

	serviceTotal = str(subprocess.check_output("systemctl list-units --all | grep 'loaded units listed'", shell=True))
	serviceTotal = serviceTotal[:-21].strip()
	serviceTotal = [int(number) for number in serviceTotal.split() if number.isdigit()]
	serviceTotal = int(''.join(map(str, serviceTotal)))
	serviceNumActive = str(subprocess.check_output("systemctl list-units --type service | grep 'loaded units listed'", shell=True))
	serviceNumActive = serviceNumActive[:-71].strip()
	serviceNumActive = [int(number) for number in serviceNumActive.split() if number.isdigit()]
	serviceNumActive = int(''.join(map(str, serviceNumActive)))
	serviceNumFailed = str(subprocess.check_output("systemctl --failed | grep 'loaded units listed'", shell=True))
	serviceNumFailed = serviceNumFailed[:-71].strip()
	serviceNumFailed = [int(number) for number in serviceNumFailed.split() if number.isdigit()]
	serviceNumFailed = int(''.join(map(str, serviceNumFailed)))

	# Print the information out

	print("Number of total loaded units: {}".format(serviceTotal))
	print("Number of total active units: {}".format(serviceNumActive))
	print("Number of total failed units: {}".format(serviceNumFailed))
	print('')

	# Getting information about each service from the service file

	if minim == False:
		for line in service:
			service[counter] = service[counter].strip()
			try:
				isActive.append(int(subprocess.check_output("systemctl status {} | grep -c 'active (running)'".format(service[counter]), shell=True)))
			except subprocess.CalledProcessError:
				print("Service {} is not active or running".format(service[counter]))
				pass
			taskNum[service[counter]] = str(subprocess.check_output("systemctl status {} | grep 'Tasks: '".format(service[counter]), shell=True))
			mainPID[service[counter]] = str(subprocess.check_output("systemctl status {} | grep 'Main PID: '".format(service[counter]), shell=True))

			# Format the strings to ensure readability

			taskNum[service[counter]] = taskNum[service[counter]].lower().strip()
			taskNum[service[counter]] = taskNum[service[counter]][6:-3]

			mainPID[service[counter]] = mainPID[service[counter]].strip()
			mainPID[service[counter]] = [int(number) for number in mainPID[service[counter]].split() if number.isdigit()]
			mainPID[service[counter]] = int(''.join(map(str, mainPID[service[counter]])))

			# Obtain process information

			mainProcHandle = psutil.Process(mainPID[service[counter]])
			mainProc = mainProcHandle.name()
			mainProcStatus = mainProcHandle.status()
			mainProcMem = mainProcHandle.memory_percent()
			mainProcCPU = mainProcHandle.cpu_percent(interval=1.0)
			totalProcMem = totalProcMem + mainProcMem
			totalProcCPU = totalProcCPU + mainProcCPU

			# Child processes go here, but that is for a future update
					
			childProcHandle = mainProcHandle.children(recursive=True)
			for child in childProcHandle:
				childProcPID[child] = int(childProcHandle[child].pid)
				childProcCPU = childProcHandle[child].cpu_percent(interval=1.0)
				childProcMemory = childProcHandle[child].memory_percent()
				totalProcCPU = totalProcCPU + childProcCPU
				totalProcMem = totalProcMem + childProcMemory

			# Now print all the information we need

			if isActive[counter] >= 1:
				print("Service: {}".format(service[counter]))
				print("Status: active and running.")
				print("Running: {}".format(taskNum[service[counter]]))
				print("Main PID of the service: {}".format(mainPID[service[counter]]))
				print("Name of main process: {}".format(mainProc))
				print("Main process status: {}".format(mainProcStatus))
				print("Main process CPU usage (percent): %f" % mainProcCPU)
				print("Main process RAM usage (percent): %f" % mainProcMem)
				print("Total service CPU usage (percent): %f" % totalProcCPU)
				print("Total service RAM usage (percent): %f" % totalProcMem)
				print('')

			else: 
				print("{} is inactive or an error has occured.".format(service[counter]))

			counter += 1


check_info()
