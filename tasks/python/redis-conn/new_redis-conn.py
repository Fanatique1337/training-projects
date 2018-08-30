#!/usr/bin/env python3

import redis
from datetime import datetime
from timeit import timeit
import psutil
from redis.connection import UnixDomainSocketConnection

# Constants:
TESTS = 10

# Initialize the parent process (the script):
#proc = psutil.Process()

# Initialize a list in which we will store the connections.
#connections = []


# Test block starting here #

pool = redis.ConnectionPool(connection_class=UnixDomainSocketConnection, path='/run/redis/redis.sock')

def timefunc():
	#global connections

	connection = redis.Redis(connection_pool=pool)
	#connection.connect()


result = timeit("timefunc()", setup="from __main__ import timefunc", number=TESTS)

# Test block ending here #
"""
# Get amount of open connections before disconnecting them:
print("Open connections: {}".format(len(proc.connections())))

# Disconnect open connections:
for conn in connections:
	conn.disconnect()

# Print open connections again to make sure they've been closed:
print("Open connections after test: {}".format(len(proc.connections())))"""

# Print results of the benchmark test:
print("Timeit result (total): {}".format(result))
print("Timeit result (average): {}".format(result / TESTS))