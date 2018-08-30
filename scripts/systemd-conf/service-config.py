#!/usr/bin/env python3

"""
NOTE:
This script requires root privileges to run.
"""

# IMPORTS:

import argparse
import configparser
import datetime
import os
import subprocess
import sys
import time

# DEFINING CONSTANTS:

VERSION = "0.1+debian-stretch"
MAINTAINER_NICKNAME = "fanatique"
MAINTAINER_EMAIL = "forcigner@gmail.com"
TRACE = True
SCHEMA = "schemas/service-config"
CONFIG = None
OUTPUT_DIR = "/etc/systemd/system"

# ERRORS:

ARGPARSE_ERR = 6
CONFIGURATION_ERR = 7
GLOBAL_ERR = 8
SCHEMA_ERR = 9
SYSTEMD_ERR = 10

# DEFAULTS:

DEFAULT_EDITOR = "vim"

DEFAULT_DESCRIPTION      = "Example"
DEFAULT_AFTER            = "network.target"
DEFAULT_TYPE             = "simple"
DEFAULT_USER             = "root"
DEFAULT_GROUP            = "root"
DEFAULT_EXEC_START       = "/bin/true"
DEFAULT_EXEC_STOP        = "/bin/true"
DEFAULT_KILL_MODE        = "control-group"
DEFAULT_KILL_SIGNAL      = "SIGTERM"
DEFAULT_PID_FILE         = None
DEFAULT_RESTART          = "on-failure"
DEFAULT_RESTART_SEC      = "2"
DEFAULT_TIMEOUT_STOP_SEC = "5"
DEFAULT_DYNAMIC_USER     = "no"
DEFAULT_ENVIRONMENT_FILE = None
DEFAULT_STANDARD_OUTPUT  = "journal"
DEFAULT_STANDARD_ERROR   = "journal"
DEFAULT_WANTED_BY        = "multi-user.target"

# COLORS AND FORMATTING:

class formatting:
	"""
	A class containing constants with most formatting/basic colors
	for Unix-based terminals and vtys.
	Does NOT work on Windows cmd, PowerShell, and their varieties!
	"""

	RESET            = "\033[0m"
	BOLD             = "\033[1m"
	DIM              = "\033[2m"
	ITALIC           = "\033[3m"
	UNDERLINE        = "\033[4m"
	BLINK            = "\033[5m" # Doesn't work on some terminals.
	INVERT           = "\033[7m"
	HIDDEN           = "\033[8m"
	FG_DEFAULT       = "\033[39m"
	FG_BLACK         = "\033[30m"
	FG_RED           = "\033[31m"
	FG_GREEN         = "\033[32m"
	FG_YELLOW        = "\033[33m"
	FG_BLUE          = "\033[34m"
	FG_MAGENTA       = "\033[35m"
	FG_CYAN          = "\033[36m"
	FG_LIGHT_GRAY    = "\033[37m"
	FG_DARK_GRAY     = "\033[90m"
	FG_LIGHT_RED     = "\033[91m"
	FG_LIGHT_GREEN   = "\033[92m"
	FG_LIGHT_YELLOW  = "\033[93m"
	FG_LIGHT_BLUE    = "\033[94m"
	FG_LIGHT_MAGENTA = "\033[95m"
	FG_LIGHT_CYAN    = "\033[96m"
	FG_WHITE         = "\033[97m"
	BG_DEFAULT       = "\033[49m"
	BG_BLACK         = "\033[40m"
	BG_RED           = "\033[41m"
	BG_GREEN         = "\033[42m"
	BG_YELLOW        = "\033[43m"
	BG_BLUE          = "\033[44m"
	BG_MAGENTA       = "\033[45m"
	BG_CYAN          = "\033[46m"
	BG_LIGHT_GRAY    = "\033[47m"
	BG_DARK_GRAY     = "\033[100m"
	BG_LIGHT_RED     = "\033[101m"
	BG_LIGHT_GREEN   = "\033[102m"
	BG_LIGHT_YELLOW  = "\033[103m"
	BG_LIGHT_BLUE    = "\033[104m"
	BG_LIGHT_MAGENTA = "\033[105m"
	BG_LIGHT_CYAN    = "\033[106m"
	BG_WHITE         = "\033[107m"


# Code starts from here:

def printf(text, f=formatting.RESET):
	"""
	A print function with formatting.
	Always prints on stdout.
	"""

	if f == 'bold':
		f = formatting.BOLD
	elif f == 'dim':
		f = formatting.DIM
	elif f == 'italic':
		f = formatting.ITALIC
	elif f == 'underline':
		f = formatting.UNDERLINE
	elif f == 'blink':
		f = formatting.BLINK
	elif f == 'invert':
		f = formatting.INVERT
	elif f == 'hidden':
		f = formatting.HIDDEN

	print("{}{}".format(f, text), file=sys.stdout)


def print_info():
	"""Print information about the script."""
	printf("This is a helper script for configuring systemd services.", f="bold")
	printf("{}Maintainer: {}{}".format(formatting.FG_GREEN, formatting.RESET, MAINTAINER_NICKNAME))
	printf("{}Email: {}{}".format(formatting.FG_GREEN, formatting.RESET, MAINTAINER_EMAIL))

def parse_arg():
	"""Get user arguments and configure them."""

	try:
		parser = argparse.ArgumentParser(description="Systemd services configuration script")
		parser.add_argument("-s",
							"--schema",
							help="Choose a custom schema and load defaults from it.",
							type=str,
							default=SCHEMA)
		parser.add_argument("--edit",
							help="Directly edit a systemd unit file.",
							action="store_true",
							default=False)
		parser.add_argument("--info",
							help="Show information about the script.",
							action="store_true",
							default=False)
		parser.add_argument("service_name",
							help="The name of the service to configure/edit.",
							type=str)

		args = parser.parse_args()

	except argparse.ArgumentError:
		print("Error: An error occured while parsing your arguments.", file=sys.stderr)
		sys.exit(ARGPARSE_ERR)

	return args

def edit(service):
	"""Open the service's systemd service unit configuration file for editing."""

	file = subprocess.check_output("systemctl show {} -p FragmentPath".format(service), shell=True)
	file = file.decode('utf-8').strip().split('=')[1]

	with subprocess.Popen(["{} {}".format(DEFAULT_EDITOR, file)], shell=True) as command:
		subprocess.Popen.wait(command)	

def setup():
	"""Check systemd version available on the host to confirm compability."""

	try:
		systemd_version = subprocess.check_output('systemd --version', shell=True)
		systemd_version = int(systemd_version.strip().split()[1])
	except subprocess.CalledProcessError:
		print("Systemd isn't working on your system. Why even use this script?", file=sys.stderr)
		sys.exit(SYSTEMD_ERR)

	return systemd_version

def load_schema(schema):

	config = configparser.ConfigParser()
	config.optionxform = str
	config.read(schema)
	config = dict(config._sections)
	config_unit = dict(config['Unit'])
	config_service = dict(config['Service'])
	config_install = dict(config['Install'])


def main():

	systemd_version = setup()
	args = parse_arg()
	if args.info:
		print_info()
	if args.edit:
		edit(args.service_name)

	load_schema(SCHEMA)

if __name__ == "__main__":
	if TRACE:
		main()
	elif not TRACE:
		try:
			main()
		except Exception as error:
			print("A global exception has been caught.", file=sys.stderr)
			print(err, file=sys.stderr)
			sys.exit(GLOBAL_ERR)

