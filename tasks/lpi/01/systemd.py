#!/usr/bin/env python3
from time import sleep
import sys
import os

with open("/var/run/lpi-01/systemd.pid", "w+") as pidfile:
	pidfile.write(str(os.getpid()))

while True:
	print("I'm aliveee!", sys.stderr)
	sleep(3600)