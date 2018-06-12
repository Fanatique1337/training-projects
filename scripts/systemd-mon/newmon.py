#!/usr/bin/env python

import sys
import os
import subprocess
import time
import getopt
import psutil

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

def main():
	minimal, cfg = parse_args()
	services = []
	services = load_services(services, cfg)
	
