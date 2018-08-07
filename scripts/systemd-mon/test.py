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
ATOP_LOGFILE = 'temp_proc_info'
SAMPLE_NUM = 2

# PID file constants

PATH_OPTIONS = ['/run/{0}/{0}.pid',
				'/run/{0}.pid',
				'/run/{0}d.pid']

FDIR_OPTIONS = ['/run/{0}', 
				'/run/{0}d']

# Zabbix MONJSON constants

VERSION = '3.0' # MONJSON version
ZBX_INTERVAL = 60
NS = "ZBX_NOTSUPPORTED"

def build_monjson(service_info, services):

	timestamp_v = int(time.time())

	output = {
		"update_interval" : "{}".format(ZBX_INTERVAL),
		"version" : VERSION,
		"applications" : {}
	}

	for service in services:

		output["applications"][service] = {}
		output["applications"][service]["name"] = "{} service".format(service)
		output["applications"][service]["items"] = {}
		output_items = output["applications"][service]["items"]

		# Build the process_name item.
		output_items["process_name"] = dict(
			name="Name of process",
			type="text",
			value=service_info[service]["name"],
			descr="Name of the service's main process",
			timestamp=timestamp_v
		)

		# Build the pid item and triggers.
		output_items["pid"] = dict(
			name="Process ID",
			type="int",
			value=service_info[service]["pid"],
			descr="",
			timestamp=timestamp_v
		)
		output_items["pid"]["triggers"] = {} 
		output_items["pid"]["triggers"]["trig1"] = dict(
			descr="SUPP: Service is not working.",
			match=-1,
			prior="err",
			resol="Check the service with systemctl status {}".format(service)
		)

		# Build the child_count item.
		output_items["child_count"] = dict(
			name="Number of child processes",
			type="int",
			value=service_info[service]["child_count"],
			descr="Amount of child processes the main process has forked.",
			timestamp=timestamp_v
		)

		# Build the status item and triggers.
		output_items["status"] = dict(
			name="Process status",
			type="text",
			value=service_info[service]["status"],
			descr="Shows the status of the process (running, sleeping, zombie, etc.)",
			timestamp=timestamp_v
		)
		output_items["status"]["triggers"] = {}
		output_items["status"]["triggers"]["trig1"] = dict(
			descr="SUPP: Main process might not be working.",
			match="^dead",
			prior="err",
			resol="Check the service and restart if needed.",
		)
		output_items["status"]["triggers"]["trig2"] = dict(
			descr="SUPP: Main process is a zombie.",
			match="^zombie",
			prior="err",
			resol="Check the service and kill if needed."
		)

		# Build memory items.
		for m_type in MEMORY_TYPES:
			output_items["memory_{}".format(m_type)] = dict(
				name="{} memory usage".format(m_type),
				type="float",
				units="%",
				value=service_info[service]["memory_{}".format(m_type)],
				descr="",
				timestamp=timestamp_v
			)

		# Build cpu_usage item and trigger.
		output_items["cpu_usage"] = dict(
			name="CPU usage of service.",
			type="float",
			units="%",
			value=service_info[service]["cpu_usage"],
			descr="",
			timestamp=timestamp_v
		)
		output_items["cpu_usage"]["triggers"] = {}
		output_items["cpu_usage"]["triggers"]["trig1"] = dict(
			descr="SUPP: Service using too much CPU.",
			range=[90, 100],
			prior="warn",
			resol="Decrease the CPU usage or ...."
		)

		# Build read_bytes item
		output_items["read_bytes"] = dict(
			name="Bytes read for the service",
			type="int",
			value=service_info[service]["read_bytes"],
			descr="",
			timestamp=timestamp_v
		)

		# Build write_bytes item
		output_items["write_bytes"] = dict(
			name="Bytes written for the service",
			type="int",
			value=service_info[service]["write_bytes"],
			descr="",
			timestamp=timestamp_v
		)

		# Build read_count item
		output_items["read_count"] = dict(
			name="Read operations for the service",
			type="int",
			value=service_info[service]["read_count"],
			descr="",
			timestamp=timestamp_v
		)

		# Build the write count item
		output_items["write_count"] = dict(
			name="Write operations for the service",
			type="int",
			value=service_info[service]["write_count"],
			descr="",
			timestamp=timestamp_v
		)

		# Build the io_read_usage item
		output_items["io_read_usage"] = dict(
			name="Read usage I/O for the service",
			type="float",
			units="%",
			value=service_info[service]["io_read_usage"],
			descr="",
			timestamp=timestamp_v
		)

		# Build the io_write_usage item
		output_items["io_write_usage"] = dict(
			name="Write usage I/O for the service",
			type="float",
			units="%",
			value=service_info[service]["io_write_usage"],
			descr="",
			timestamp=timestamp_v
		)

		output["applications"][service]["items"] = output_items

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

	return args

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

def setup():
	time_now = datetime.datetime.now()
	time_delta = time_now - datetime.timedelta(minutes=SAMPLE_NUM-1)
	time_begin = '{}:{}'.format(time_delta.hour, time_delta.minute)
	time_end = '{}:{}'.format(time_now.hour, time_now.minute) 

	exit_code = subprocess.call("atop -P PRD,DSK -b {} -e {} -r > {}".format(time_begin, time_end, ATOP_LOGFILE), shell=True)

	disk_lines = []
	read_counts = []
	write_counts = []
	total_read_count = 0
	total_write_count = 0

	with open(ATOP_LOGFILE, "r") as source_file:
		source = source_file.readlines()

	for line in source:
		if line.startswith('DSK'):
			disk_lines.append(line)

	for disk_line in disk_lines:
		source.remove(disk_line)
		line_info = disk_line.strip().split(' ')
		read_counts.append(line_info[8])
		write_counts.append(line_info[10])

	for reads in read_counts:
		total_read_count += int(reads)
	for writes in write_counts:
		total_write_count += int(writes)

	return exit_code, source, (total_read_count, total_write_count)

class ProcMon:

	def __init__(self, service_pid):
		self.pid = service_pid
		self.process = psutil.Process(service_pid)
		with self.process.oneshot():
			self.childs = self.process.children(recursive=True)
			self.name = self.process.name()
			self.child_num = len(self.childs)
			self.status = self.process.status()
			self.io_stats = self.process.io_counters()
			self.cpu_usage = self.process.cpu_percent(interval=0.01)
			self.memory_rss = self.process.memory_percent(memtype="rss")
			self.memory_vms = self.process.memory_percent(memtype="vms")
			self.memory_swap = self.process.memory_percent(memtype="swap")
			for child in self.childs:
				self.cpu_usage += child.cpu_percent(interval=0.01)
				self.memory_rss += child.memory_percent(memtype="rss")
				self.memory_vms += child.memory_percent(memtype="vms")
				self.memory_swap += child.memory_percent(memtype="swap")

	def get_process_name(self):
		return self.name

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

	def get_status(self):
		return self.process.status()

	def get_io_usage(self, source, disk_ops):
		proc_reads = 0
		proc_writes = 0

		for line in source:
			for child in self.childs:
				if ' {} ({})'.format(self.pid, self.name) in line or ' {} ('.format(child.pid) in line:
					line = line.strip().split(' ')
					proc_reads += int(line[11])
					proc_writes += int(line[13])


		if disk_ops[0] > 0:
			io_read = (proc_reads / disk_ops[0]) * 100
		else:
			io_read = 0
		if disk_ops[1] > 0:
			io_write = (proc_writes / disk_ops[1]) * 100
		else:
			io_write = 0

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
			print("The service {} most probably does not exist or is not running.".format(service))
			mainpid = -1

		mainpid = -1

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
	args = parse_arg() 
	services = load_services(args.config) # Get the services into the list by using the cfg file.
	setup_code, parse_source, disk_ops = setup()

	for service in services:
		service_info[service] = {}
		service_info[service]["pid"] = get_pid(service)
		if service_info[service]["pid"] > 0:
			proc = ProcMon(service_info[service]["pid"])
			service_info[service]["name"] = proc.name
			service_info[service]["child_count"] = proc.child_num
			service_info[service]["cpu_usage"] = proc.cpu_usage
			service_info[service]["memory_vms"] = proc.memory_vms
			service_info[service]["memory_rss"] = proc.memory_rss
			service_info[service]["memory_swap"] = proc.memory_swap
			service_info[service]["status"] = proc.status
			io_stats = proc.io_stats
			service_info[service]["read_bytes"] = io_stats.read_bytes
			service_info[service]["write_bytes"] = io_stats.write_bytes
			service_info[service]["read_count"] = io_stats.read_count
			service_info[service]["write_count"] = io_stats.write_count
			if setup_code == 0:
				io_usage = proc.get_io_usage(parse_source, disk_ops)
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
			for t in args.memtypes:
				service_info[service]["memory_{}".format(t)] = NS
			service_info[service]["read_bytes"] = NS
			service_info[service]["write_bytes"] = NS
			service_info[service]["read_count"] = NS
			service_info[service]["write_count"] = NS
			service_info[service]["io_read_usage"] = NS
			service_info[service]["io_write_usage"] = NS

	#print(json.dumps(service_info, indent=4, sort_keys=True))
	print(json.dumps(build_monjson(service_info, services), indent=4, sort_keys=False))

	if args.benchmark:
		print("Time ran: {}".format(datetime.datetime.now() - start_time))


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

