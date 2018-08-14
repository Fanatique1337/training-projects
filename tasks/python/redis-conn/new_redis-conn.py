#!/usr/bin/env python3

import redis
from datetime import datetime
from timeit import timeit
import psutil

# Constants:
TESTS = 10

# Initialize the parent process (the script):
proc = psutil.Process()

# Initialize a list in which we will store the connections.
connections = []


# Test block starting here #

def timefunc():
	global connections

	connection = redis.Connection(host='localhost', port=6379, db=0)
	connection.connect()
	connections.append(connection)

result = timeit("timefunc()", setup="from __main__ import timefunc", number=TESTS)

# Test block ending here #

# Get amount of open connections before disconnecting them:
print("Open connections: {}".format(len(proc.connections())))

# Disconnect open connections:
for conn in connections:
	conn.disconnect()

# Print open connections again to make sure they've been closed:
print("Open connections after test: {}".format(len(proc.connections())))

# Print results of the benchmark test:
print("Timeit result (total): {}".format(result))
print("Timeit result (average): {}".format(result / TESTS))