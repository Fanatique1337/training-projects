#!/usr/bin/env python3

import signal
import sys

def handler(signal, frame):
    print("Caught {}".format(signal))
    sys.exit(0)

while True:
    signal.signal(signal.SIGINT, handler)
    signal.alarm(5)