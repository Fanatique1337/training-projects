#!/usr/bin/env python

# Exit codes:
# 6	:	Getopt Error. Probably wrong argument or misspell.
# 7 : 	TBA
# 8	:	TBA

import sys
import os
import subprocess
import time
import getopt
import psutil
from datetime import datetime
sys.tracebacklimit = 1000
# Get arguments and set configuration
startTime = datetime.now()

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
		try:
			mainpid = int(subprocess.check_output("systemctl status {} | grep 'Main PID: ' | grep -Eo '[[:digit:]]*' | head -n 1".format(svc), shell=True))
		except ValueError as e:
			pass
		try:
			mainproc = psutil.Process(mainpid)
			mchildren = mainproc.children(recursive=True)
			pidchecks.append(mainpid)
			for child in mchildren:
				pidchecks.append(child.pid)
		except psutil._exceptions.NoSuchProcess:
			print("No running process with pid {} ({}). Probably the service isn't working.\n".format(str(mainpid), svc))
		except psutil._exceptions.ZombieProcess:
			print("The process with pid {} ({}) is a zombie process\n".format(str(mainpid), svc))
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
		print("Memory usage of process {}: {}%\n".format(entry, memdic[entry]))

main()


#print("Time ran: {}".format(datetime.now() - startTime))