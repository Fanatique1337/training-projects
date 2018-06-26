#!/usr/bin/env python


import os
import sys

perms = str(sys.argv[1])
filepath = str(sys.argv[2])
perms = int(perms, 8)
os.chmod(filepath, perms)
