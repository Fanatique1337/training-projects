#!/usr/bin/env python


import os
import sys

perms = str(sys.argv[1])
filepath = str(sys.argv[2])
print(filepath)
print(perms)
perms = oct(perms)
print(perms)

os.chmod(filepath, perms)