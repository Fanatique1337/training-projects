#!/usr/bin/env python3

import redis
from datetime import datetime
import timeit

pool = redis.ConnectionPool(host='localhost', port=6379, db=0, max_connections=10000)
connection = redis.StrictRedis(connection_pool=pool)

def timefunc():

	newconn = redis.StrictRedis(connection_pool=pool)
	print("Open connections during test: {}".format(len(connection.client_list())))

startTime = datetime.now()

timeit_result = timeit.timeit("timefunc()", setup="from __main__ import timefunc", number=10)

print("Open connections after finishing test: {}".format(len(connection.client_list())))
print("Time ran with pool: {}".format(datetime.now() - startTime))
print("Python timeit: {}".format(timeit_result))

