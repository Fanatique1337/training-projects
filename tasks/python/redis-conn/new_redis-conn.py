#!/usr/bin/env python3

import redis
from datetime import datetime
import timeit
import psutil

proc = psutil.Process()

test_num = 10

def timefunc():
	connection = redis.Connection(host='localhost', port=6379, db=0)
	connection.connect()
	print("Open connections: {}".format(len(proc.connections())))
	connection.disconnect()

timeit_result = timeit.timeit("timefunc()", setup="from __main__ import timefunc", number=test_num)
print("Open connections after test: {}".format(len(proc.connections())))

print("Timeit result (total): {}".format(timeit_result))
print("Timeit result (average): {}".format(timeit_result / test_num))