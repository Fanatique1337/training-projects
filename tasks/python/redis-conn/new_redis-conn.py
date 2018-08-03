#!/usr/bin/env python3

import redis
from datetime import datetime
import timeit

test_num = 5000

def timefunc():
	connection = redis.Connection(host='10.20.1.115', port=6379, db=0)
	connection.connect()
	connection.disconnect()


timeit_result = timeit.timeit("timefunc()", setup="from __main__ import timefunc", number=test_num)

print("Timeit result (total): {}".format(timeit_result))
print("Timeit result (average): {}".format(timeit_result / test_num))