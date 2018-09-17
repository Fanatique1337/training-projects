#!/usr/bin/env python3

import redis
from datetime import datetime
from timeit import timeit
from redis.connection import UnixDomainSocketConnection

import systemd_service_mon as monitor

# Constants:
TESTS = 10

# Test block starting here #

pool = redis.ConnectionPool(connection_class=UnixDomainSocketConnection, path='/run/redis/redis.sock')
connection = redis.Redis(connection_pool=pool)
pub_sub = connection.pubsub()
results = []

redis_pid = monitor.get_pid('redis-server')

def timefunc(pubstring):
    connection.publish('benchmark_channel', pubstring)

startstring = 'a'
pubstring = 'a'
while True:
    result = timeit("timefunc('{}')".format(pubstring), setup="from __main__ import timefunc", number=1)
    redis_server = monitor.ProcMon(redis_pid)
    cpu_usage = redis_server.cpu_usage
    memory_vms = redis_server.memory_vms_b
    memory_rss = redis_server.memory_rss_b
    memory_swap = redis_server.memory_swap_b
    print("String size: {:<10} [|] Time taken: {:<22} [|] CPU usage: {:<4} [|] RAM usage: {:<4}".format(len(pubstring), result, redis_server.cpu_usage, redis_server.memory_rss_b))
    results.append(result)

# Test block ending here #

# Print results of the benchmark test:
print("Timeit result (total): {}".format(sum(results)))
print("Timeit result (average): {}".format(sum(results) / float(len(results))))
print("All results:")
for res in results:
    print(res)