#!/usr/bin/env python

# Exit codes:
# 6	:	Getopt Error. Probably wrong argument or misspell.
# 7	: 	TBA
# 8	:	TBA

# Import default system libraries.

import getopt
import os
import subprocess
import sys
# from datetime import datetime # Uncomment if going to benchmark for speed.

# Import external libraries.

import psutil
from pathlib import Path

# startTime = datetime.now() # Start the timer for benchmarking. Must uncomment last line as well.

# Get arguments and set configuration.

def parse_args():
	cfgfile = 'smon.conf'
	minimal = False

	if len(sys.argv) > 1:
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'mc:', ['minimal=', 'config='])
		except getopt.GetoptError:
			print("An error occured while parsing your arguments. Check the proper usage of the script.")
			sys.exit(6)

		for opt, arg in opts:
			if opt in ('-m', '--minimal'):
				minimal = True
			if opt in ('-c', '--config'):
				cfgfile = str(arg)

	return minimal, cfgfile

# Read services from the configuration file and add them into a list.

def load_services(handlerlist, cfg):
	with open(cfg, "r") as servfile:
		for line in servfile:
			handlerlist.append(line.strip())
	return handlerlist

# Read CPU and Memory usage of the processes.

def read_stats(ss):
	cpud = {}
	memd = {}

	for pid in ss:

		# CPU times and usage can be found in the /proc/ filesystem in stat files.

		with open(os.path.join('/proc/', str(pid), 'stat'), 'r') as pfile: 
			pidtimes = pfile.read().split(' ')
			pname = str(pidtimes[1])[1:-1]
			utime = int(pidtimes[13]) # utime is the 14th element in the stat file (man proc).
			stime = int(pidtimes[14]) # stime is the 15th element in the stat file (man proc).
			pidtotal = utime - stime

		with open('/proc/stat', 'r') as cfile: # Get total system CPU times.
			cputimes = cfile.readline().split(' ')
			cputotal = 0
			for integ in cputimes[2:]:
				integ = int(integ)
				cputotal = cputotal + integ

		usg = (pidtotal / cputotal) * 100 # Process CPU usage is process cpu times / system cpu time.

		if usg < 0: # Deny negative values
			usg = 0

		cpud[pname] = str(usg) # A major bug here. Have to fix. For each PID it rewrites the usage..
		phandler = psutil.Process(pid) # Generate a process class for the given PID.
		pmem = phandler.memory_percent() # Get memory usage in percents of services.
		memd[pname] = str(pmem)

	return cpud, memd

# Get the Process ID for each service in the configuration file. 

def get_pid(slist):
	pidchecks = [] # Predefine the list of PIDs.

	for svc in slist:

		cpuusage = 0 # Predefine the variable for CPU usage.

		try: # For every service, try to find its PID file in /var/run and read it.
			pidfpath = '/var/run/{}/{}.pid'.format(svc, svc)
			if not Path(pidfpath).exists(): # Most services have a /var/run/service/service.pid file.
				pidfpath = '/var/run/{}.pid'.format(svc)
				if not Path(pidfpath).exists(): # Others have a /var/run/service.pid file.
					pidfolder = '/var/run/{}'.format(svc)
					tmpc = os.listdir(pidfolder)
					for f in tmpc: # And others have various pidfiles like /var/run/service/pid.
						f = str(f)
						if 'pid' in f:
							pidfpath = pidfolder + '/' + f # Add the file to the dir path. 

			with open(pidfpath, 'r') as pidf:
				mainpid = int(pidf.readline().strip()) # Read the PID number. Not sure if strip is needed. Have to check.

		except Exception as e: # If such a PID file does not exist, get Main PID from parsing systemctl.
			try:
				mainpid = int(subprocess.check_output("systemctl status {} | grep 'Main PID: ' | grep -Eo '[[:digit:]]*' | head -n 1".format(svc), shell=True))
			except ValueError as e: # If systemctl returns nothing, then such a service does not exist.
				pass

		try: # Get all the children of the Main PID and append them to a list.
			mainproc = psutil.Process(mainpid)
			mchildren = mainproc.children(recursive=True)
			pidchecks.append(mainpid)
			for child in mchildren:
				pidchecks.append(child.pid)
		except psutil._exceptions.NoSuchProcess: # Return an error if there is no such process working.
			print("No running process with pid {} ({}). Probably the service isn't working.\n".format(str(mainpid), svc))
		except psutil._exceptions.ZombieProcess: # Return an error if the process is a zombie process.
			print("The process with pid {} ({}) is a zombie process\n".format(str(mainpid), svc))

	return pidchecks

def main():
	minimal, cfg = parse_args() # Get arguments for minimal mode and for the configuration file.
	services = [] # Predefine the services list.
	services = load_services(services, cfg) # Get the services into the list by using the cfg file.
	pidlist = get_pid(services) # Get PIDs of the services' processes.
	cpudic = {} # Predefine the dictionary for CPU usage.
	memdic = {} # Predefine the dictionary for RAM usage.
	cpudic, memdic = read_stats(pidlist) # Get stats into the dictionary.
	for (entry, usg) in cpudic.items(): # Print the results.
		print("CPU usage of process {}: {}%".format(entry, usg))
		print("Memory usage of process {}: {}%\n".format(entry, memdic[entry]))

main() # No need for main module check.


# print("Time ran: {}".format(datetime.now() - startTime)) # Uncomment if going to benchmark.
