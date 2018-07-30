#!/usr/bin/env python3

import redis
from datetime import datetime
import timeit

pool = redis.ConnectionPool(host='localhost', port=6379, db=0, max_connections=101)

def timefunc():

	connection = redis.StrictRedis(connection_pool=pool)
	return connection.client_list()

startTime = datetime.now()

timeit_result = timeit.timeit("timefunc()", setup="from __main__ import timefunc", number=100)

print("Time ran with pool: {}".format(datetime.now() - startTime))
print("Python timeit: {}".format(timeit_result))
