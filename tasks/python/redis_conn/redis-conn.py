#!/usr/bin/env python3

import redis
from datetime import datetime
from timeit import timeit
from redis.connection import UnixDomainSocketConnection

import systemd_service_mon as monitor

# Constants:
TESTS = 10
FILE = 'packets.dat'

def get_times(pid):
    with open('/proc/stat', 'r') as sysfile:
        cpu = sysfile.readline().strip().split()
        system_user_time   = int(cpu[1])
        system_system_time = int(cpu[3])

    with open('/proc/{}/stat'.format(pid), 'r') as redisfile:
        cpuline = redisfile.readline().strip().split()
        redis_user_time   = int(cpuline[13])
        redis_system_time = int(cpuline[14])

    return system_user_time, system_system_time, redis_user_time, redis_system_time

def calculate_cpu(start, end):
    times_usage_user   = end[0] - start[0]
    times_usage_kernel = end[1] - start[1]

    redis_times_user   = end[2] - start[2]
    redis_times_kernel = end[3] - start[3]

    if times_usage_user > 0:
        redis_user_usage = (redis_times_user / times_usage_user) * 100
    else:
        redis_user_usage = 0
    if times_usage_kernel > 0:
        redis_kernel_usage = (redis_times_kernel / times_usage_kernel) * 100.
    else:
        redis_kernel_usage = 0

    return redis_user_usage, redis_kernel_usage

# Test block starting here #
redis_pid = monitor.get_pid('redis-server')

pool = redis.ConnectionPool(connection_class=UnixDomainSocketConnection, path='/run/redis/redis.sock')
connection = redis.Redis(connection_pool=pool)
pub_sub = connection.pubsub()
results = []


def timefunc(pubstring):
    connection.publish('benchmark_channel', pubstring)

print("String size,Time taken,CPU usage (user), CPU usage (kernel), Memory (RSS), Memory (VMS)")
with open(FILE, 'r') as inputfile:
    for x in range(50):
        packet = inputfile.readline().strip()
        start_times = get_times(redis_pid)
        result = timeit("timefunc('{}')".format(packet), setup="from __main__ import timefunc", number=TESTS) / TESTS
        end_times = get_times(redis_pid)
        redis_server = monitor.ProcMon(redis_pid)
        cpu_usage = calculate_cpu(start_times, end_times)
        memory_vms = redis_server.memory_vms_b
        memory_rss = redis_server.memory_rss_b
        memory_swap = redis_server.memory_swap_b
        memory_shared = redis_server.memory_shared
        print("{0:<10},{1:<22},{2:<6.2f},{3:<6.2f},{4:<9},{5:<8}".format(len(packet), result, cpu_usage[0], cpu_usage[1], memory_rss, memory_vms))
        results.append(result)
        if result > 1:
            print("Reached 1s, aborting.")
            break

# Test block ending here #
