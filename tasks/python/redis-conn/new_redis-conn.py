#!/usr/bin/env python3

import redis
from datetime import datetime
import timeit

def timefunc():
	connection = redis.StrictRedis(host='localhost', port=6379, db=0)
	return connection.client_list()

startTime = datetime.now()

timeit_result = timeit.timeit("timefunc()", setup="from __main__ import timefunc", number=100)

print("Time ran without pool: {}".format(datetime.now() - startTime))
print("Python timeit: {}".format(timeit_result))