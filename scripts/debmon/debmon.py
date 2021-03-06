#!/usr/bin/env python3

# Exit codes:
# 6:	Argparse Error. Probably a wrong/mistyped argument.
# 7:	Global exception caught. Could be anything.

import aiohttp
import apt
import argparse
import asyncio
import glob
import json
import os
import subprocess
import sys

# Error constants

ARGPARSE_ERR = 6
GLOBAL_ERR = 7

# Other constants

CONFIG = 'debmon.conf'

async def parse_arg():
	"""Get arguments and set the configuration."""

	try:
		parser = argparse.ArgumentParser(description="Debian package and source monitoring")
		parser.add_argument("-c",
							"--config",
							help="Specify an input configuration file.",
							type=str,
							default=CONFIG)
		parser.add_argument("--ignore-http-status",
							help="If specified, ignores the return http status error codes.",
							action="store_true",
							default=False)
		args = parser.parse_args()

	except argparse.ArgumentError:
		print("An error occurred while parsing your arguments.", file=sys.stderr)
		sys.exit(ARGPARSE_ERR)

	return args.config, args.ignore_http_status

async def get_sources(allowed_urls):
	"""Get trusted and untrusted package sources."""

	used_sources = {}
	unallowed_sources = []
	sourcefiles = ['/etc/apt/sources.list']
	sourcefiles.extend(glob.glob('/etc/apt/sources.list.d/*.list'))

	for src in sourcefiles:
		with open(src, "r") as src_file:
			lines = src_file.readlines()
		for line in lines:
			if 'deb [arch' in line or 'deb http' in line:
				line = line.split(' ')
				for keyword in line:
					if keyword.startswith('http'):
						url = keyword.strip()
						if url in allowed_urls and url not in used_sources:
							used_sources[url] = await get_stat_code(url)
						elif url not in allowed_urls:
							print("Unallowed source URL in {}: {}".format(src, url), 
								  file=sys.stderr)
							unallowed_sources.append(url)

	return used_sources

async def get_stat_code(url):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			if response.status == 403 or response.status == 404:
				print("The URL {} returns an error code {}".format(url, response.status), 
					  file=sys.stderr)
			return response.status

async def get_local_pkgs():
	temp_output = subprocess.check_output("apt list --installed 2> /dev/null | grep 'installed,local'", shell=True)
	return temp_output.decode('utf-8')

async def main():
	config, ignore_bool = await parse_arg()
	with open(config, "r") as conf_file:
		allowed_sources = conf_file.readlines()

	allowed_sources = [src.strip() for src in list(filter(lambda x: x.startswith('http'), allowed_sources))]
	used_sources = await get_sources(allowed_sources)

	print(json.dumps(used_sources, sort_keys=True, indent=4))

	local_pkgs = await get_local_pkgs()
	print(local_pkgs)

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())