#!/usr/bin/env python3
from chardet import detect

ATOP_HIST = '/var/log/atop/atop_20180731'

with open(ATOP_HIST, "rb") as file:
	det = detect(file.read())

print(det)