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
			print("An error occured while parsing your arguments.")
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

def read_stats(ss, cpudic):
	cpudic = {}
	for pid in ss:
		with open(os.path.join('/proc/', str(pid), 'stat'), 'r') as pfile:
			pidtimes = pfile.read().split(' ')
			print(pidtimes)
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
		cpudic[str(pid)] = str(usg)
	return cpudic

def get_pid(slist):
	pidchecks = []
	for svc in slist:
		cpuusage = 0
		mainpid = int(subprocess.check_output("systemctl status {} | grep 'Main PID: ' | grep -Eo '[[:digit:]]*' | head -n 1".format(svc), shell=True))
		mainproc = psutil.Process(mainpid)
		mparent = mainproc.parent()
		mchildren = mparent.children(recursive=True)
		for child in mchildren:
			pidchecks.append(child.pid)
	return pidchecks

def main():
	minimal, cfg = parse_args()
	services = ['ssh']
	services = load_services(services, cfg)
	pidlist = get_pid(services)
	cpudic = {}
	cpudic = read_stats(pidlist, cpudic)
	print(cpudic)

main()