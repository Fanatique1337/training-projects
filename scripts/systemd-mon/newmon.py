#!/usr/bin/env python

import sys
import os
import subprocess
import time
import getopt
import psutil
sys.tracebacklimit = 1000
# Get arguments and set configuration

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

def load_services(handlerlist, cfg):
	with open(cfg, "r") as servfile:
		for line in servfile:
			handlerlist.append(line.strip())
	return handlerlist

def read_stats(ss):
	cpud = {}
	memd = {}
	for pid in ss:
		with open(os.path.join('/proc/', str(pid), 'stat'), 'r') as pfile:
			pidtimes = pfile.read().split(' ')
			#print(pidtimes)
			pname = str(pidtimes[1])[1:-1]
			#print(pname)
			utime = int(pidtimes[13])
			stime = int(pidtimes[14])
			pidtotal = utime - stime

		with open('/proc/stat', 'r') as cfile:
			cputimes = cfile.readline().split(' ')
			cputotal = 0
			for integ in cputimes[2:]:
				integ = int(integ)
				cputotal = cputotal + integ
		usg = (pidtotal / cputotal) * 100
		if usg < 0:
			usg = 0
		cpud[pname] = str(usg)

		phandler = psutil.Process(pid)
		pmem = phandler.memory_percent()
		memd[pname] = str(pmem)

	return cpud, memd

def get_pid(slist):
	pidchecks = []
	for svc in slist:
		cpuusage = 0
		mainpid = int(subprocess.check_output("systemctl status {} | grep 'Main PID: ' | grep -Eo '[[:digit:]]*' | head -n 1".format(svc), shell=True))
		try:
			mainproc = psutil.Process(mainpid)
			mchildren = mainproc.children(recursive=True)
			pidchecks.append(mainpid)
			for child in mchildren:
				pidchecks.append(child.pid)
		except psutil._exceptions.NoSuchProcess:
			print("No running process with pid {}. Probably the service isn't working.".format(str(mainpid)))
		except psutil._exceptions.ZombieProcess:
			print("The process with pid {} is a zombie process".format(str(mainpid)))
	return pidchecks

def main():
	minimal, cfg = parse_args()
	services = []
	services = load_services(services, cfg)
	pidlist = get_pid(services)
	cpudic = {}
	memdic = {}
	cpudic, memdic = read_stats(pidlist)
	for (entry, usg) in cpudic.items():
		print("CPU usage of process {}: {}%".format(entry, usg))
		print("Memory usage of process {}: {}%".format(entry, memdic[entry]))
		print("")

main()