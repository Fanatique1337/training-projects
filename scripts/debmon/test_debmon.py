#!/usr/bin/env python3

# Exit codes:
# 6:	Argparse Error. Probably a wrong/mistyped argument.
# 7:	Global exception caught. Could be anything.

import apt
import argparse
import glob
import json
import os
import subprocess
import sys
import urllib

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
							help="If specified, ignores the return http status error codes.",
							action="store_true",
							default=False)
		args = parser.parse_args()

	except argparse.ArgumentError:
		print("An error occurred while parsing your arguments.", file=sys.stderr)
		sys.exit(ARGPARSE_ERR)

	return args.config, args.ignore_http_status

def get_sources(allowed_urls):
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
							used_sources[url] = get_stat_code(url)
						elif url not in allowed_urls:
							print("Unallowed source URL in {}: {}".format(src, url), 
								  file=sys.stderr)
							unallowed_sources.append(url)

	return used_sources

def get_stat_code(url):
	status = 0
	try:
		with urllib.request.urlopen(url) as session:
			status = session.getcode()
	except urllib.error.HTTPError as error:
			print("The URL {} returns an error code {}.".format(url, error.code), 
				  file=sys.stderr)
			status = error.code
	return status

def get_local_pkgs():
	temp_output = subprocess.check_output("apt list --installed | grep 'installed,local' 2> /dev/null", shell=True)
	return temp_output.decode('utf-8')

def main():
	config, ignore_bool = parse_arg()
	with open(config, "r") as conf_file:
		allowed_sources = conf_file.readlines()

	allowed_sources = [src.strip() for src in list(filter(lambda x: x.startswith('http'), allowed_sources))]
	used_sources = get_sources(allowed_sources)

	print(json.dumps(used_sources, sort_keys=True, indent=4))

	local_pkgs = get_local_pkgs()

	print(local_pkgs)

if __name__ == "__main__":
	main()