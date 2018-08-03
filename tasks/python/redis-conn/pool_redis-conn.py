#!/usr/bin/env python3

import redis
from datetime import datetime
import timeit

pool = redis.ConnectionPool(host='localhost', port=6379, db=0, max_connections=10000)

def timefunc():
    connection = redis.Redis(connection_pool=pool)


startTime = datetime.now()
timeit_result = timeit.timeit("timefunc()", setup="from __main__ import timefunc", number=10000)
print("Time ran with pool: {}".format(datetime.now() - startTime))
print("Python timeit: {}".format(timeit_result))

