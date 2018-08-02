#!/usr/bin/env python3

import redis
from datetime import datetime
import timeit

interface = redis.StrictRedis(host='localhost', port=6379, db=0)

def timefunc():

	connection = redis.Connection(host='localhost', port=6379, db=0)
	connection.connect()
	connection.disconnect()
	print("Open connections during test: {}".format(len(interface.client_list())))

startTime = datetime.now()

timeit_result = timeit.timeit("timefunc()", setup="from __main__ import timefunc", number=10)

print("Open connections after finishing test: {}".format(len(interface.client_list())))
print("Time ran without pool: {}".format(datetime.now() - startTime))
print("Python timeit: {}".format(timeit_result))
