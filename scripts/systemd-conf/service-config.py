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

from collections import OrderedDict

# DEFINING CONSTANTS:

VERSION             = "0.2"
MAINTAINER_NICKNAME = "fanatique"
MAINTAINER_EMAIL    = "forcigner@gmail.com"
TRACE               = True
SCHEMA              = "schemas/service-config"
SCHEMA_SHORT        = "schemas/short_service-config"
SCHEMA_EXTENDED     = "schemas/extended_service-config"
CONFIG              = None
OUTPUT_DIR          = "/etc/systemd/system"

# ERRORS:

ARGPARSE_ERR        = 6
CONFIGURATION_ERR   = 7
GLOBAL_ERR          = 8
SCHEMA_ERR          = 9
SYSTEMD_ERR         = 10
UID_ERROR           = 11
FINISH_ERROR        = 12

# DEFAULTS:

DEFAULT_EDITOR           = "vim"
DEFAULT_BUILD_SCHEMA     = "schemas/default-schema"

DEFAULT_DESCRIPTION      = "Example"
DEFAULT_AFTER            = "network.target"
DEFAULT_TYPE             = "simple"
DEFAULT_USER             = "root"
DEFAULT_GROUP            = "root"
DEFAULT_EXEC_START       = "/bin/true"
DEFAULT_EXEC_STOP        = "/bin/true"
DEFAULT_KILL_MODE        = "control-group"
DEFAULT_KILL_SIGNAL      = "SIGTERM"
DEFAULT_PID_FILE         = "/run/service.pid"
DEFAULT_RESTART          = "on-failure"
DEFAULT_RESTART_SEC      = "2"
DEFAULT_TIMEOUT_STOP_SEC = "5"
DEFAULT_DYNAMIC_USER     = "no"
DEFAULT_ENVIRONMENT_FILE = "/etc/service/env"
DEFAULT_STANDARD_OUTPUT  = "journal"
DEFAULT_STANDARD_ERROR   = "journal"
DEFAULT_WANTED_BY        = "multi-user.target"

# COLORS AND Formatting:

class Formatting:
	"""
	A class containing constants with most Formatting/basic colors
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

def tty_supports_ansi(): # TO DO - implement it so it disables formatting if not supported

	for handle in [sys.stdout, sys.stderr]:
		if ((hasattr(handle, "isatty") and handle.isatty()) or
		    ('TERM' in os.environ and os.environ['TERM'] == "ANSI")):
		    return True
		else:
			return False

def printf(text, f=Formatting.RESET, **kwargs):
	"""
	A print function with Formatting.
	Always prints on stdout.
	"""

	if f == 'bold':
		f = Formatting.BOLD
	elif f == 'dim':
		f = Formatting.DIM
	elif f == 'italic':
		f = Formatting.ITALIC
	elif f == 'underline':
		f = Formatting.UNDERLINE
	elif f == 'blink':
		f = Formatting.BLINK
	elif f == 'invert':
		f = Formatting.INVERT
	elif f == 'hidden':
		f = Formatting.HIDDEN

	print("{}{}".format(f, text), file=sys.stdout, **kwargs)


def print_info():
	"""Print information about the script."""
	printf("This is a helper script for configuring systemd services.", f="bold")
	printf("{}Maintainer: {}{}".format(Formatting.FG_GREEN, Formatting.RESET, MAINTAINER_NICKNAME))
	printf("{}Email: {}{}".format(Formatting.FG_GREEN, Formatting.RESET, MAINTAINER_EMAIL))

	sys.exit(0)

def parse_arg():
	"""Get user arguments and configure them."""

	parser = argparse.ArgumentParser(description="Systemd services configuration script")
	schema = parser.add_mutually_exclusive_group()
	build = parser.add_mutually_exclusive_group()
	parser.add_argument("-c",
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
	build.add_argument("-b",
						"--build",
						help="Builds a default schema in schemas/default-schema",
						action="store_true",
						default=False)
	schema.add_argument("-s",
						"--short",
						help="Use a short configuration schema.",
						action="store_true",
						default=False)
	schema.add_argument("-x",
						"--extended",
						help="Use a long configuration schema.",
						action="store_true",
						default=False)
	schema.add_argument("-d",
						"--directory",
						help="Output directory for the service unit file.",
						type=str,
						default=OUTPUT_DIR)
	build.add_argument("service_name",
						help="The name of the service to configure/edit.",
						type=str,
						nargs='?')

	try:
		args = parser.parse_args()
		if not args.service_name and not args.build:
			print("You need to supply a positional argument: service name.")
			parser.print_usage()
			sys.exit(ARGPARSE_ERR)
	except argparse.ArgumentError:
		print("Error: An error occured while parsing your arguments.", file=sys.stderr)
		sys.exit(ARGPARSE_ERR)

	return args

def edit(service, manual=False, finish=True):
	"""Open the service's systemd service unit configuration file for editing."""

	if manual:
		file = service
	else:
		file = subprocess.check_output("systemctl show {} -p FragmentPath".format(service), shell=True)
		file = file.decode('utf-8').strip().split('=')[1]

	with subprocess.Popen(["{} {}".format(DEFAULT_EDITOR, file)], shell=True) as command:
		subprocess.Popen.wait(command)

	if finish: 
		finish(file, mode="edit")

def setup(args):
	"""Check systemd version available on the host to confirm compability."""

	try:
		systemd_version = subprocess.check_output('systemd --version', shell=True)
		systemd_version = int(systemd_version.strip().split()[1])
	except subprocess.CalledProcessError:
		print("Systemd isn't working on your system. Why even use this script?", file=sys.stderr)
		sys.exit(SYSTEMD_ERR)

	if os.getuid() > 0 and not args.build and args.directory == OUTPUT_DIR:
		printf("{}Insufficient permissions. You have to run the script as root (with sudo).".format(Formatting.FG_LIGHT_RED), f="bold")
		sys.exit(UID_ERROR)

	#if tty_supports_ansi():
		#print("supports ansi") # TO DO

	return systemd_version

def build():
	if os.path.exists(DEFAULT_BUILD_SCHEMA):
		print("Error: {} already exists.".format(DEFAULT_BUILD_SCHEMA), file=sys.stderr)
		sys.exit(SCHEMA_ERR)
	else:
		schema = configparser.ConfigParser()
		schema.optionxform = str
		schema['Unit'] = OrderedDict(
			Description     = DEFAULT_DESCRIPTION,
			After           = DEFAULT_AFTER
		)

		schema['Service'] = OrderedDict(
			Type            = DEFAULT_TYPE,
			ExecStart       = DEFAULT_EXEC_START,
			ExecStop        = DEFAULT_EXEC_STOP,
			Restart         = DEFAULT_RESTART,
			RestartSec      = DEFAULT_RESTART_SEC,
			User            = DEFAULT_USER,
			Group           = DEFAULT_GROUP,
			PIDFile         = DEFAULT_PID_FILE,
			EnvironmentFile = DEFAULT_ENVIRONMENT_FILE,
			KillMode        = DEFAULT_KILL_MODE,
			KillSignal      = DEFAULT_KILL_SIGNAL,
			TimeoutStopSec  = DEFAULT_TIMEOUT_STOP_SEC,
			StandardOutput  = DEFAULT_STANDARD_OUTPUT,
			StandardError   = DEFAULT_STANDARD_ERROR,
			DynamicUser     = DEFAULT_DYNAMIC_USER
		)

		schema['Install'] = OrderedDict(
			WantedBy        = DEFAULT_WANTED_BY
		)

		with open(DEFAULT_BUILD_SCHEMA, 'w+') as schemafile:
			schema.write(schemafile)

		finish(DEFAULT_BUILD_SCHEMA, mode="build")

def load_schema(schema):

	config_dict = {}

	config = configparser.ConfigParser()
	config.optionxform = str
	config.read(schema)

	return config

def parse_config(cfg):

	config = argparse.Namespace(**OrderedDict(cfg))
	config.Unit = OrderedDict(config.Unit)
	config.Service = OrderedDict(config.Service)
	config.Install = OrderedDict(config.Install)

	return config

def write_config(cfg, destination):
	config = configparser.ConfigParser()
	config.optionxform = str
	config['Unit'] = cfg.Unit
	config['Service'] = cfg.Service
	if cfg.Install:
		config['Install'] = cfg.Install
	with open(destination, 'w') as unitfile:
		config.write(unitfile)
		unitfile.write("#Automatically generated by service-config.\n")

def user_configuration(config):

	user_config = config

	printf("{}[Unit] section configuration:".format(Formatting.FG_YELLOW), f="bold")
	for key in config.Unit:
		printf("{}{}={}".format(Formatting.FG_GREEN, key, Formatting.RESET), f="bold", end="")
		value = input()
		user_config.Unit[key] = value

	print()
	printf("{}[Service] section configuration:".format(Formatting.FG_BLUE), f="bold")
	for key in config.Service:
		printf("{}{}={}".format(Formatting.FG_GREEN, key, Formatting.RESET), f="bold", end="")
		value = input()
		user_config.Service[key] = value

	print()
	printf("{}[Install] section configuration:".format(Formatting.FG_MAGENTA), f="bold")
	for key in config.Install:
		printf("{}{}={}".format(Formatting.FG_GREEN, key, Formatting.RESET), f="bold", end="")
		value = input()
		user_config.Install[key] = value

	user_config.Unit = {k: v for k, v in user_config.Unit.items() if v}
	user_config.Service = {k: v for k, v in user_config.Service.items() if v}
	user_config.Install = {k: v for k, v in user_config.Install.items() if v}

	return user_config

def enable_service(service):
	subprocess.call('systemctl daemon-reload', shell=True)
	subprocess.call('systemctl enable {}'.format(service), shell=True)

def start_service(service):
	subprocess.call('systemctl daemon-reload', shell=True)
	subprocess.call('systemctl start {}'.format(service), shell=True)

def finish(destination, mode="create"):
	if os.path.exists(destination):
		if mode == "create":
			print("{}Service created successfully.".format(Formatting.FG_GREEN))
		elif mode == "edit":
			print("{}Service edited successfully.".format(Formatting.FG_YELLOW))
		elif mode == "build":
			print("{}Default schema built successfully.".format(Formatting.FG_BLUE))
		sys.exit(0)
	else:
		print("The script failed to finish successfully.")
		sys.exit(FINISH_ERROR)

def main():

	args = parse_arg()
	systemd_version = setup(args)

	if args.info:
		print_info()
	if args.build:
		build()
	if args.edit:
		edit(args.service_name)
	if args.short:
		args.schema = SCHEMA_SHORT
		print("Using short schema configuration.")
	if args.extended:
		args.schema = SCHEMA_EXTENDED
		print("Using extended schema configuration.")

	schema = load_schema(args.schema)
	config = parse_config(schema)
	user_config = user_configuration(config)

	destination = os.path.join(args.directory, '{}.service'.format(args.service_name))
	write_config(user_config, destination)

	print("Do you want to manually edit the new configuration? [y/N]: ", end="")
	manual = input()
	if manual and manual.lower() == "y":
		edit(destination, manual=True, finish=False)

	if os.getuid() == 0:
		print("Do you want to enable the service? [y/N]: ", end="")
		enable = input()
		if enable and enable.lower() == "y":
			enable_service(args.service_name)
		print("Do you want to start the service? [Y/n]: ", end="")
		start = input()
		if not start or (start and start.lower() == "y"):
			start_service(args.service_name)
	elif os.getuid() > 0:
		print("{}No permissions to enable/start service. Need to run with root privileges.".format(Formatting.FG_RED))

	finish(destination)

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

