#!/usr/bin/env python3

# Exit codes:
# 6	:	Argparse Error. Probably wrong argument or misspell.
# 7	: 	Global exception caught. Could be anything.

from __future__ import print_function
import argparse
import os
import subprocess
import sys
from datetime import datetime # Uncomment if going to benchmark for speed.

import psutil

# Error constants

ARGPARSE_ERR = 6
GLOBAL_ERR = 7

# Stat file constants

PROC_NAME = 1
PROC_UTIME = 13
PROC_STIME = 14

# Other constants

CONFIG = 'smon.conf'

def parse_arg():
	"""Get arguments and set configuration."""

	try:
		parser = argparse.ArgumentParser(description="systemd service monitor")
		parser.add_argument("-c", 
							"--config", 
							help="Use a different configuration file, not default ({})".format(CONFIG), 
							type=str,
							default=CONFIG)
		parser.add_argument("-b",
							"--benchmark",
							help="Benchmark the script's runtime",
							action="store_true",
							default=False)
		args = parser.parse_args()

	except argparse.ArgumentError:
		print(("An error occured while parsing your arguments. "
			   "Check the proper usage of the script."), file=sys.stderr)
		sys.exit(ARGPARSE_ERR)

	return args.config, args.benchmark

def load_services(cfg):
	"""Read services from the configuration file and add them into a list."""

	handler_list = [] # Predefine the list for services.
	try:
		with open(cfg, "r") as servfile:
			for line in servfile:
				handler_list.append(line.strip())
	except:
		print("The file {} most probably does not exist. ".format(cfg), 
			  file=sys.stderr)

	return handler_list

def read_stats(service_pids):
	"""Read CPU and Memory usage of the processes."""

	cpud = {}
	memd = {}

	for pid in service_pids:

		with open(os.path.join('/proc/', str(pid), 'stat'), 'r') as pfile: 
			pidtimes = pfile.read().split(' ')
			pname = str(pidtimes[1])[1:-1]

		cpud[pname] = '0'
		memd[pname] = '0'

	for pid in service_pids:

		# CPU times and usage can be found in the /proc/ filesystem in stat files.

		with open(os.path.join('/proc/', str(pid), 'stat'), 'r') as pfile: 
			pidtimes = pfile.read().split(' ')
			pname = str(pidtimes[PROC_NAME])[1:-1]
			utime = int(pidtimes[PROC_UTIME])
			stime = int(pidtimes[PROC_STIME])
			pidtotal = utime - stime

		with open('/proc/stat', 'r') as cfile: # Get total system CPU times.
			cputimes = cfile.readline().split(' ')
			cputotal = 0
			for integ in cputimes[2:]:
				integ = int(integ)
				cputotal = cputotal + integ

		# Process CPU usage is process cpu times / system cpu time.
		usage = (pidtotal / cputotal) * 100 

		if usage < 0: # Deny negative values
			usage = 0

		newusage = float(cpud[pname]) + usage
		cpud[pname] = str(newusage) # Calculate the usage and add to it.
		phandler = psutil.Process(pid) # Generate a process class for the given PID.
		pmem = phandler.memory_percent() # Get memory usage in percents of services.
		newpmem = float(memd[pname]) + pmem
		memd[pname] = str(newpmem)

	return cpud, memd

def get_pid(slist):
	"""Get the Process ID for each service in the configuration file. """

	pidchecks = [] # Predefine the list of PIDs.

	for service in slist:

		try: # For every service, try to find its PID file in /var/run and read it.
			pidfpath = get_pidf_path(service)
			with open(pidfpath, 'r') as pidfile:
				mainpid = int(pidfile.readline()) # Read the PID number.

		except OSError: # If such a PID file does not exist, get Main PID from parsing systemctl.
			try:
				mainpid = int(subprocess.check_output(("systemctl status {} | grep 'Main PID: ' | "
					"grep -Eo '[[:digit:]]*' | head -n 1").format(service), shell=True))
			except ValueError: # If systemctl returns nothing, then such a service does not exist.
				pass

		try: # Get all the children of the Main PID and append them to a list.
			main_proc = psutil.Process(mainpid)
			pidchecks.append(mainpid)
			for child in main_proc.children(recursive=True):
				pidchecks.append(child.pid)
		except psutil.NoSuchProcess: # Return an error if there is no such process working.
			print(("No running process with pid {} ({}). "
				   "Probably the service isn't working.\n").format(str(mainpid), service),
					file=sys.stderr)
		except psutil.ZombieProcess: # Return an error if the process is a zombie process.
			print("The process with pid {} ({}) is a zombie process\n".format(str(mainpid), service),
					file=sys.stderr)

	return pidchecks

def get_pidf_path(service):
	"""Check if a pidfile exists in /var/run"""
	# Most services do store their pids in a /var/run/service/service.pid file
	pidfpath = '/var/run/{}/{}.pid'.format(service, service)
	if os.path.exists(pidfpath):
		return pidfpath

	# Other services have a /var/run/service.pid file
	pidfpath = '/var/run/{}.pid'.format(service)
	if os.path.exists(pidfpath):
		return pidfpath

	# Some add a 'd' to their names for 'daemon'
	pidfpath = '/var/run/{}.pid'.format(service + 'd')
	if os.path.exists(pidfpath):
		return pidfpath

	# Others have a /var/run/service file
	pidfpath = '/var/run/{}'.format(service)
	if os.path.exists(pidfpath) and os.path.isfile(pidfpath):
		return pidfpath

	# And with a 'd'..
	pidfpath = '/var/run/{}'.format(service + 'd')
	if os.path.exists(pidfpath):
		if os.path.isdir(pidfpath):
			for file in os.listdir(pidfpath):
				if 'pid' in str(file):
					pidfpath = os.path.join(pidfpath, file)
					if os.path.isfile(pidfpath):
						return pidfpath
		elif os.path.isfile(pidfpath):
			return pidfpath

	# And others have various pidfiles like /var/run/service/pid
	pidfolder = '/var/run/{}'.format(service)
	for file in os.listdir(pidfolder):
		if 'pid' in str(file):
			pidfpath = os.path.join(pidfolder, file)
			if os.path.isfile(pidfpath):
				return pidfpath

def main():
	cfg, benchmark = parse_arg() # Get arguments for minimal mode and for the configuration file.
	services = load_services(cfg) # Get the services into the list by using the cfg file.
	pidlist = get_pid(services) # Get PIDs of the services' processes.
	cpudic, memdic = read_stats(pidlist) # Get stats into the dictionary.
	for (entry, usage) in cpudic.items(): # Print the results.
		print("CPU usage of process {}: {}%".format(entry, usage))
		print("Memory usage of process {}: {}%\n".format(entry, memdic[entry]))

	if benchmark:
		print("Time ran: {}".format(datetime.now() - startTime))

try:
	if __name__ == "__main__":
		startTime = datetime.now() # Start the timer for benchmarking. 
		main()
except Exception as err:
	print("A global exception has occured.", file=sys.stderr)
	print(err, file=sys.stderr)
	sys.exit(GLOBAL_ERR)

