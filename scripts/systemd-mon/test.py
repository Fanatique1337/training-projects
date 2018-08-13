#!/usr/bin/env python3

import psutil

proc = psutil.Process(655)

rss = proc.memory_percent(memtype="rss")
print(rss)

vms = proc.memory_percent(memtype="vms")
print(vms)

with open('/proc/meminfo', 'r') as total:
	content = total.readlines()

for line in content:
	if line.startswith('SwapTotal:'):
		line = line.strip().split()
		print(line[1])

with open('/proc/655/status', 'r') as current:
	content = current.readlines()

for line in content:
	if line.startswith('VmSwap'):
		line = line.strip().split()
		print(line)

