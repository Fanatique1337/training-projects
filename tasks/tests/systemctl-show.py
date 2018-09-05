#!/usr/bin/env python3
from timeit import timeit

result = timeit("subprocess.call('systemctl show dnsmasq > /dev/null', shell=True)", setup="import subprocess", number=1000)

print("{}ms per call".format(result))