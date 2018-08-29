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

VERSION = "0.1"
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

# DEFAULTS:

DEFAULT_DESCRIPTION = "Example"
DEFAULT_AFTER = "network.target"
DEFAULT_TYPE = "simple"
DEFAULT_USER = "root"
DEFAULT_GROUP = "root"
DEFAULT_EXEC_START = "/bin/true"
DEFAULT_EXEC_STOP = "/bin/true"
DEFAULT_KILL_MODE = "control-group"
DEFAULT_KILL_SIGNAL = "SIGTERM"
DEFAULT_PID_FILE = None
DEFAULT_RESTART = "on-failure"
DEFAULT_RESTART_SEC = "2"
DEFAULT_TIMEOUT_STOP_SEC = "5"
DEFAULT_DYNAMIC_USER = "no"
DEFAULT_ENVIRONMENT_FILE = None
DEFAULT_STANDARD_OUTPUT = "journal"
DEFAULT_STANDARD_ERROR = "journal"
DEFAULT_WANTED_BY = "multi-user.target"
