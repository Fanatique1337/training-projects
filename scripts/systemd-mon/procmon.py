#!/usr/bin/env python
import sys
import psutil
import subprocess

# Defining global variables #



# Using get_pid we get a PID of the process name #

def get_pid(process):
	return int(subprocess.check_output(["pidof", "-s", process]))

# Defining the gather information function #

def info():
	process = input("What is the name of the process?: ")
	procPID = get_pid(process) # getting the PID
	proc = psutil.Process(procPID) # initializing the process
	procName = proc.name() # storing the process name
	procParent = proc.parent() # initializing parent process
	procParentName = procParent.name() # storing parent process name
	procParentID = procParent.pid # storing parent process PID
	procStatus = proc.status() # storing process status
	procCPU = proc.cpu_percent(interval=1.0) # storing process CPU usage
	procCore = proc.cpu_num() # storing process' main core
	procMemory = proc.memory_percent() # store process' memory usage

	# And print them.. #

	print("Process name:", procName)
	print("Process ID:", procPID)
	print("Process Parent Name and ID:", procParentName, procParentID)
	print("The process is", procStatus)
	print("CPU usage(%):", procCPU)
	print("Process running on CPU core", procCore)
	print("Memory usage(%):", procMemory)

# Using functions to ensure easy scalability #

info()
