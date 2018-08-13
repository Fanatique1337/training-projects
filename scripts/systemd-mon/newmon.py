#!/usr/bin/env python3

# Exit codes:
# 6	:	Argparse Error. Probably wrong argument or misspell.
# 7	: 	Global exception caught. Could be anything.

from __future__ import print_function
import argparse
import datetime
import json
import os
import subprocess
import sys
import time

import psutil

# atop PRD constants

PRD_READ = -8 # the read stat is the 8th column from right to left
PRD_WRITE = -6 # the write stat is the 6th column from right to left

# Error constants

ARGPARSE_ERR = 6
GLOBAL_ERR = 7
CONF_ERR = 8
CALL_ERR = 9

# PID file constants # Options where to search for the PID file

PATH_OPTIONS = ['/run/{0}/{0}.pid',
				'/run/{0}.pid',
				'/run/{0}d.pid']

FDIR_OPTIONS = ['/run/{0}', 
				'/run/{0}d']

# Zabbix MONJSON constants

VERSION = '3.0' # MONJSON version
ZBX_INTERVAL = 60 # Call interval used by zabbix agent.
NS = "ZBX_NOTSUPPORTED" # Value for values that cannot be gathered.

# Other constants

CONFIG = 'config.json' # Default configuration file.
TRACE = True # Should we traceback errors | False to catch global exceptions
MEMORY_TYPES_BYTES = ['vms', 'rss', 'swap'] # Types of memory to be monitored.
MEMORY_TYPES_PERCENT = ['rss', 'swap']
ATOP_LOGFILE = 'temp_proc_info' # Temporary file to save the atop history to.
SAMPLE_NUM = 2 # Number of samples to get from atop history.

def build_monjson(service_info, service, output):
	"""Build the MONJSON output format."""

	timestamp_v = int(time.time())

	output["name"] = "systemd service: {}".format(service)
	output["items"] = {}
	output_items = output["items"]

	# Build the process_name item.
	output_items["process_name"] = dict(
		name="Process: name",
		type="text",
		value=service_info["name"],
		descr="Name of the service's main process",
		timestamp=timestamp_v
	)

	# Build the pid item and triggers.
	output_items["pid"] = dict(
		name="Process: ID",
		type="int",
		value=service_info["pid"],
		descr="",
		timestamp=timestamp_v
	)
	output_items["pid"]["triggers"] = {} 
	output_items["pid"]["triggers"]["trig1"] = dict(
		descr="SUPP: Service is not working.",
		range=[-1, -1],
		prior="warn",
		resol="Check the service with systemctl status {}".format(service)
	)

	# Build the child_count item.
	output_items["child_count"] = dict(
		name="Process: Number of children",
		type="int",
		value=service_info["child_count"],
		descr="Amount of child processes the main process has forked.",
		timestamp=timestamp_v
	)

	# Build the status item and triggers.
	output_items["status"] = dict(
		name="Process: Status",
		type="text",
		value=service_info["status"],
		descr="Shows the status of the process (running, sleeping, zombie, etc.)",
		timestamp=timestamp_v
	)
	output_items["status"]["triggers"] = {}
	output_items["status"]["triggers"]["trig1"] = dict(
		descr="SUPP: Main process might not be working.",
		match="^dead",
		prior="warn",
		resol="Check the service and restart if needed.",
	)
	output_items["status"]["triggers"]["trig2"] = dict(
		descr="SUPP: Main process is a zombie.",
		match="^zombie",
		prior="warn",
		resol="Check the service and kill if needed."
	)

	# Build memory items.
	for m_type in MEMORY_TYPES_PERCENT:
		output_items["memory_{}_p".format(m_type)] = dict(
			name="Memory (percent): {}".format(m_type),
			type="float",
			units="%",
			value=service_info["memory_{}_p".format(m_type)],
			descr="",
			timestamp=timestamp_v
		)
		output_items["memory_{}_p".format(m_type)]["triggers"] = {}
		output_items["memory_{}_p".format(m_type)]["triggers"]["trig1"] = dict(
			descr="SUPP: Memory usage is too high!",
			resol="Get creative.",
			range=[90, 100],
			prior="warn"
		)

	for mb_type in MEMORY_TYPES_BYTES:
		output_items["memory_{}_b".format(mb_type)] = dict(
			name="Memory (bytes): {}".format(mb_type),
			type="int",
			units="B",
			value=service_info["memory_{}_b".format(mb_type)],
			descr="",
			timestamp=timestamp_v
		)

	# Build cpu_usage item and trigger.
	output_items["cpu_usage"] = dict(
		name="CPU: usage",
		type="float",
		units="%",
		value=service_info["cpu_usage"],
		descr="",
		timestamp=timestamp_v
	)
	output_items["cpu_usage"]["triggers"] = {}
	output_items["cpu_usage"]["triggers"]["trig1"] = dict(
		descr="SUPP: Service using too much CPU.",
		range=[90, 100],
		prior="warn",
		resol="Decrease the CPU usage."
	)

	# Build read_bytes item
	output_items["read_bytes"] = dict(
		name="I/O: bytes read",
		type="int",
		value=service_info["read_bytes"],
		descr="",
		timestamp=timestamp_v
	)

	# Build write_bytes item
	output_items["write_bytes"] = dict(
		name="I/O: bytes written",
		type="int",
		value=service_info["write_bytes"],
		descr="",
		timestamp=timestamp_v
	)

	# Build read_count item
	output_items["read_count"] = dict(
		name="I/O: read ops",
		type="int",
		value=service_info["read_count"],
		descr="",
		timestamp=timestamp_v
	)

	# Build the write count item
	output_items["write_count"] = dict(
		name="I/O: write ops",
		type="int",
		value=service_info["write_count"],
		descr="",
		timestamp=timestamp_v
	)

	# Build the io_read_usage item and triggers
	output_items["io_read_usage"] = dict(
		name="I/O: read usage",
		type="float",
		units="%",
		value=service_info["io_read_usage"],
		descr="",
		timestamp=timestamp_v
	)
	output_items["io_read_usage"]["triggers"] = {}
	output_items["io_read_usage"]["triggers"]["trig1"] = dict(
		descr="SUPP: The service is using too much read I/O.",
		resol="Insert creative resolution here",
		range=[90, 100],
		prior="warn"
	)

	# Build the io_write_usage item and triggers
	output_items["io_write_usage"] = dict(
		name="I/O: write usage",
		type="float",
		units="%",
		value=service_info["io_write_usage"],
		descr="",
		timestamp=timestamp_v
	)
	output_items["io_write_usage"]["triggers"] = {}
	output_items["io_write_usage"]["triggers"]["trig1"] = dict(
		descr="SUPP: The service is using too much write I/O.",
		resol="Insert creative resolution here",
		range=[90, 100],
		prior="warn"
	)

	output["items"] = output_items

	return output

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

		args = parser.parse_args()

	except argparse.ArgumentError:
		print(("An error occured while parsing your arguments. "
			   "Check the proper usage of the script."), file=sys.stderr)
		sys.exit(ARGPARSE_ERR)

	return args

def load_services(cfg):
	"""Read services from the configuration file and add them into a list."""

	handler_list = [] # Predefine the list for services.
	conf_dict = {} # Predefine the dictionary with configurable services.

	try:
		with open(cfg, "r") as servfile:
			conf_data = json.load(servfile)

	except OSError:
		print("The file {} most probably does not exist. ".format(cfg), 
			  file=sys.stderr)
		sys.exit(CONF_ERR)

	for key, value in conf_data.items():
		handler_list.append(key)
		if value["manual"] == 1:
			conf_dict[key] = value

	return handler_list, conf_dict

def setup():
	time_now = datetime.datetime.now()
	time_delta = time_now - datetime.timedelta(minutes=SAMPLE_NUM-1)
	time_begin = '{}:{}'.format(time_delta.hour, time_delta.minute)
	time_end = '{}:{}'.format(time_now.hour, time_now.minute) 

	exit_code = subprocess.call("atop -P PRD -b {} -e {} -r > {}".format(time_begin, time_end, ATOP_LOGFILE), shell=True)
	if exit_code == 127:
		print("The atop tool most probably is not installed or cannot be found.", file=sys.stderr)
		sys.exit(CALL_ERR)

	with open(ATOP_LOGFILE, "r") as source_file:
		source = source_file.readlines()

	return exit_code, source

class ProcMon:
	"""
	The process class to gather information about a single process and its children.
	Information gathered:
	* Main process' children
	* Main process name
	* Number of childrens running # currently unused
	* Main process status (running, dead, zombie..)
	* IO counters since boot
	* CPU usage (percent)
	* Resident memory usage (percent)
	* Swap memory usage (percent)
	* Virtual memory size (bytes)

	CPU and Memory usages are total for the main process + its children, 
	since we are monitoring a service and not a single process.
	"""

	def __init__(self, service_pid):
		"""Initialize the class and efficiently gather starting information about the process."""
		self.pid = service_pid
		self.process = psutil.Process(service_pid)
		with self.process.oneshot(): # Use psutil's process caching method to increase performance.
			self.childs = self.process.children(recursive=True)
			self.name = self.process.name()
			self.child_num = len(self.childs) 
			self.status = self.process.status()
			self.io_stats = self.process.io_counters()
			self.cpu_usage = self.process.cpu_percent(interval=0.01)
			self.meminfo = self.process.memory_full_info()
			self.memory_rss_p = self.process.memory_percent(memtype="rss")
			self.memory_vms_b = self.meminfo.vms # We want VMS in bytes, not percents.
			self.memory_swap_p = self.process.memory_percent(memtype="swap")
			self.memory_rss_b = self.meminfo.rss
			self.memory_swap_b = self.meminfo.swap
			for child in self.childs: # Get total CPU/Memory usage for the process' children.
				self.cpu_usage += child.cpu_percent(interval=0.01)
				self.meminfo_c = self.process.memory_full_info()
				self.memory_rss_p += child.memory_percent(memtype="rss")
				self.memory_vms_b += self.meminfo_c.vms
				self.memory_swap_p += child.memory_percent(memtype="swap")
				self.memory_rss_b += self.meminfo_c.rss
				self.memory_swap_b += self.meminfo_c.swap

	def get_io_usage(self, source):
		"""
		Get the total I/O usage of all processes, as well as the I/O usage
		for the specified process. I am aware that getting the total I/O usage
		for all processes every time this function is being called for a process
		is an unneccessary overhead. However, if I moved the total I/O stats in
		the setup() function, I'd have to iterate over the source two times. 
		And the source is a list with 3000+ lines parsed from atop's history file. 
		Iterating over this list only once is a performance bonus in contrast to
		doing it twice.

		[source] here must be a list of strings, each string representing a line from
		atop's history generated with the PRD parseable output label.

		In this function we iterate over the source lines from atop's history file,
		and add the number of reads & writes to the totals for every line. If the line
		is for the process we're using this function for, we add the line's write & read
		count to those of the process as well.
		"""

		proc_reads = 0
		proc_writes = 0

		total_reads = 0
		total_writes = 0

		for line in source: 
			is_current = False
			if line.startswith('PRD'):
				if '({})'.format(self.name) in line:
					is_current = True
				line = line.strip().split(' ')
				total_reads += int(line[PRD_READ])
				total_writes += int(line[PRD_WRITE])
				if is_current:
					proc_reads += int(line[PRD_READ])
					proc_writes += int(line[PRD_WRITE])

		io_read = (proc_reads / total_reads) * 100 if total_reads > 0 else 0
		io_write = (proc_writes / total_writes) * 100 if total_writes > 0 else 0

		return (io_read, io_write)


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
			print("The service {} most probably does not exist or is not running.".format(service), file=sys.stderr)
			mainpid = -1

	return mainpid

def get_pidf_path(service):
	"""Check if a pidfile exists in the /run directory"""

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
	"""
	The main function responsible for controlling the arguments and the whole information gathering.
	"""
	service_info = {}

	# Get arguments for minimal mode and for the configuration file.
	args = parse_arg() 
	services, conf_dict = load_services(args.config) # Get the services into the list by using the cfg file.
	setup_code, parse_source = setup()

	output = {
		"update_interval" : "{}".format(ZBX_INTERVAL),
		"version" : VERSION,
		"applications" : {}
	}

	for service in services:
		service_info[service] = {}
		service_info[service]["pid"] = get_pid(service)
		if service_info[service]["pid"] > 0:
			proc = ProcMon(service_info[service]["pid"])
			service_info[service]["name"] = proc.name
			service_info[service]["child_count"] = proc.child_num
			service_info[service]["cpu_usage"] = proc.cpu_usage
			service_info[service]["memory_vms_b"] = proc.memory_vms_b
			service_info[service]["memory_rss_p"] = proc.memory_rss_p
			service_info[service]["memory_swap_p"] = proc.memory_swap_p
			service_info[service]["memory_rss_b"] = proc.memory_rss_b
			service_info[service]["memory_swap_b"] = proc.memory_swap_b
			service_info[service]["status"] = proc.status
			io_stats = proc.io_stats
			service_info[service]["read_bytes"] = io_stats.read_bytes
			service_info[service]["write_bytes"] = io_stats.write_bytes
			service_info[service]["read_count"] = io_stats.read_count
			service_info[service]["write_count"] = io_stats.write_count
			if setup_code == 0:
				io_usage = proc.get_io_usage(parse_source)
				service_info[service]["io_read_usage"] = io_usage[0]
				service_info[service]["io_write_usage"] = io_usage[1]
			else:
				service_info[service]["io_read_usage"] = NS
				service_info[service]["io_write_usage"] = NS
		elif service_info[service]["pid"] == -1:
			service_info[service]["status"] = NS
			service_info[service]["name"] = NS
			service_info[service]["child_count"] = NS
			service_info[service]["cpu_usage"] = NS
			for t in MEMORY_TYPES_BYTES:
				service_info[service]["memory_{}_b".format(t)] = NS
				service_info[service]["memory_{}_p".format(t)] = NS
			service_info[service]["read_bytes"] = NS
			service_info[service]["write_bytes"] = NS
			service_info[service]["read_count"] = NS
			service_info[service]["write_count"] = NS
			service_info[service]["io_read_usage"] = NS
			service_info[service]["io_write_usage"] = NS

		output["applications"][service] = {}
		output["applications"][service] = build_monjson(
			service_info[service], 
			service, 
			output["applications"][service]
		)
		
		if service in conf_dict:
			for key, value in conf_dict[service].items():
				if key != "manual":
					output["applications"][service]["items"][key]["triggers"] = value["triggers"]


	print(json.dumps(output))

	if args.benchmark:
		print("Time ran: {}".format(datetime.datetime.now() - start_time), file=sys.stderr)


if __name__ == "__main__":
	start_time = datetime.datetime.now()
	if TRACE:
		main()
	else:
		try:
			main()
		except Exception as err:
			print("A global exception has been caught.", file=sys.stderr)
			print(err, file=sys.stderr)
			sys.exit(GLOBAL_ERR)

