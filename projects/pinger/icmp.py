#!/usr/bin/env python
import subprocess
import json
from pprint import pprint

def get_json():
	with open('icmp_ping_input.json') as data_file:
		data = json.load(data_file)
	return data

def main():
	data = get_json()
	ip = str(data["applications"]["icmp_ping"]["pings"]["google"]["address"])
	ip = ip.split('.')
	ip[2] = ip[2].replace("/", "")
	address = ip[1] + '.' + ip[2]
	preload = data["applications"]["icmp_ping"]["pings"]["google"]["packets_rate"]
	timeout = data["applications"]["icmp_ping"]["pings"]["google"]["packets_timeout"]
	amount = data["applications"]["icmp_ping"]["pings"]["google"]["packets_count"]
	ping(address, preload, timeout, amount)
	dict_iteration(data)


def dict_iteration(data):
	counter = 0
	addr = ['']

	for key, value in data.items():
		if isinstance(value, dict):
			dict_iteration(value)
		else:
			if key == 'address':
				addr[counter] = value
				print(addr[counter])
				counter = counter + 1

def ping(address, preload, timeout, count):
	if int(preload) > 0:
		subprocess.call("ping {} -c {} -W {} -l {} | tail -n 2 > icmp-log.txt".format(address, count, timeout, preload), shell=True)
	else:
		subprocess.call("ping {} -c {} -W {} | tail -n 2 > icmp-log.txt".format(address, count, timeout), shell=True)
	
	build_output()


def parse_output():
	with open('icmp-log.txt') as data_file:
		data = data_file.readlines()
	
	data[0] = data[0].strip().split(',')
	data[1] = data[1].strip().split('/')

	rtt = data[1][4]
	mdev = data[1][6][:-3]
	packet_loss = data[0][2][1:-12]

	print("RTT average: {} (ms), RTT mdev: {} (ms), Packet loss: {}".format(rtt, mdev, packet_loss))
	return rtt, mdev, packet_loss

def build_output():
	rtt_value, mdev_value, packet_loss = parse_output()
	
	
main()
