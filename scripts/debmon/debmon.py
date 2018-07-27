#!/usr/bin/env python3

# Exit codes:
# 6:	Argparse Error. Probably a wrong/mistyped argument.
# 7:	Global exception caught. Could be anything.

import aiohttp
import apt
import argparse
import asyncio
import glob
import os
import sys

# Error constants

ARGPARSE_ERR = 6
GLOBAL_ERR = 7

# Other constants

CONFIG = 'debmon.conf'

def parse_arg():
	"""Get arguments and set the configuration."""

	try:
		parser = argparse.ArgumentParser(description="Debian package and source monitoring")
		parser.add_argument("-c",
							"--config",
							help="Specify an input configuration file.",
							type=str,
							default=CONFIG)
		parser.add_argument("--ignore-http-status",
							help="If specified, ignores the return http status code.",
							action="store_true",
							default=False)
		args = parser.parse_args()

	except argparse.ArgumentError:
		print("An error occurred while parsing your arguments.", file=sys.stderr)
		sys.exit(ARGPARSE_ERR)

	return args.config, args.ignore-http-status

def get_sources():
	"""Get trusted and untrusted package sources."""

	sourcefiles = ['/etc/apt/sources.list']
	sourcefiles.append(glob.glob('/etc/apt/sources.list.d/*.list'))

	for src in sourcefiles:
		with open(src, "r") as src_file:
			lines = src_file.readlines()
		for line in lines:
			if line.contains('deb '):
				line = line.split(' ')
				for keyword in line

get_sources()