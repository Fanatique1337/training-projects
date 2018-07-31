#!/usr/bin/env python3

# Exit codes:
# 6	:	Argparse Error. Probably wrong argument or misspell.
# 7	: 	Global exception caught. Could be anything.

from __future__ import print_function
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

import psutil

# Error constants

ARGPARSE_ERR = 6
GLOBAL_ERR = 7

# Stat file constants

PROC_NAME = 1
PROC_UTIME = 13
PROC_STIME = 14

# Other constants

CONFIG = '/etc/monithor/smon.conf'
TRACE = True
MEMORY_TYPES = ['vms', 'rss', 'swap']

# PID file constants

PATH_OPTIONS = ['/run/{0}/{0}.pid',
				'/run/{0}.pid',
				'/run/{0}d.pid']

FDIR_OPTIONS = ['/run/{0}', 
				'/run/{0}d']


def parse_arg():
	"""Get arguments and set configuration."""

	try:
		parser = argparse.ArgumentParser(description="systemd service monitor")
		parser.add_argument("-c", 
							"--config", 
							help="Use the specified configuration file.",
							type=str,
							default=CONFIG)
		parser.add_argument("-b",
							"--benchmark",
							help="Benchmark the script's runtime",
							action="store_true",
							default=False)
		parser.add_argument("-m",
							"--memtypes",
							help="Choose memory types (vms/rss/uss/pss/swap) to monitor.",
							nargs="+",
							default=MEMORY_TYPES)
		args = parser.parse_args()

	except argparse.ArgumentError:
		print(("An error occured while parsing your arguments. "
			   "Check the proper usage of the script."), file=sys.stderr)
		sys.exit(ARGPARSE_ERR)

	return args.config, args.benchmark, args.memtypes

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

class ProcMon:

	def __init__(self, service_pid):
		self.process = psutil.Process(service_pid)
		self.childs = self.process.children(recursive=True)

	def get_process_name(self):
		return self.process.name()

	def get_child_pids(self):
		child_pids = []
		for child in self.childs:
			child_pids.append(child.pid)
		return child_pids

	def get_child_num(self):
		return len(self.childs)

	def get_cpu_usage(self):
		cpu_usage = self.process.cpu_percent(interval=0.01)
		for child in self.childs:
			cpu_usage += child.cpu_percent(interval=0.01)
		return cpu_usage

	def get_memory_usage(self, m_type):
		memory_usage = self.process.memory_percent(memtype=m_type)
		for child in self.childs:
			memory_usage += child.memory_percent(memtype=m_type)
		return memory_usage

	def get_io_stats(self):
		return self.process.io_counters()


def get_pid(service):
	"""Get the Process ID for each service in the configuration file. """

	try: # For every service, try to find its PID file in /run and read it.
		pidfpath = get_pidf_path(service)
		with open(pidfpath, 'r') as pidfile:
			mainpid = int(pidfile.readline()) # Read the PID number.

	# If such a PID file does not exist, get Main PID from parsing systemctl.
	except (OSError, TypeError): 
		try:
			mainpid = int(subprocess.check_output(("systemctl status {} | grep 'Main PID: ' | "
				"grep -Eo '[[:digit:]]*' | head -n 1").format(service), shell=True))
		except ValueError: # If systemctl returns nothing, then such a service does not exist.
			print("The service {} most probably does not exist.".format(service))


	except psutil.NoSuchProcess: # Return an error if there is no such process working.
		print(("No running process with pid {} ({}). "
			   "Probably the service isn't working.\n").format(str(mainpid), service),
				file=sys.stderr)
	except psutil.ZombieProcess: # Return an error if the process is a zombie process.
		print("The process with pid {} ({}) is a zombie process\n".format(str(mainpid), service),
				file=sys.stderr)

	return mainpid

def get_pidf_path(service):
	"""Check if a pidfile exists in /run directory"""

	for filepath in PATH_OPTIONS:
		path = filepath.format(service)
		if os.path.exists(path):
			return path

	for dirpath in FDIR_OPTIONS:
		path = dirpath.format(service)
		if os.path.exists(path) and os.path.isdir(path):
			for file in os.listdir(path):
				if 'pid' in str(file):
					return os.path.join(path, file)


def main():
	service_info = {}

	# Get arguments for minimal mode and for the configuration file.
	cfg, benchmark, memory_types = parse_arg() 
	services = load_services(cfg) # Get the services into the list by using the cfg file.

	for service in services:
		service_info[service] = {}
		service_info[service]["pid"] = get_pid(service)
		proc = ProcMon(service_info[service]["pid"])
		service_info[service]["name"] = proc.get_process_name()
		service_info[service]["child_count"] = proc.get_child_num()
		service_info[service]["cpu_usage"] = proc.get_cpu_usage()
		for t in memory_types:
			service_info[service]["memory_{}".format(t)] = proc.get_memory_usage(t)
		service_info[service]["running"] = proc.process.is_running()
		io_stats = proc.get_io_stats()
		service_info[service]["read_bytes"] = io_stats.read_bytes
		service_info[service]["write_bytes"] = io_stats.write_bytes
		service_info[service]["read_count"] = io_stats.read_count
		service_info[service]["write_count"] = io_stats.write_count

	print(json.dumps(service_info, indent=4, sort_keys=True))

	if benchmark:
		print("Time ran: {}".format(datetime.now() - startTime))


if __name__ == "__main__":
	startTime = datetime.now()
	if TRACE:
		main()
	else:
		try:
			main()
		except Exception as err:
			print("A global exception has been caught.", file=sys.stderr)
			print(err, file=sys.stderr)
			sys.exit(GLOBAL_ERR)