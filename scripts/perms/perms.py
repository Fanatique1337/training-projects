#!/usr/bin/env python


import os
import sys

from pathlib import Path as path

def main():

	if len(sys.argv) < 2:
		
		print("Correct usage: ")
		prusg()

	else:

		perms = str(sys.argv[1])
		if '-h' in perms or 'help' in perms:
			prusg()
			sys.exit(5)
		if not perms.isdigit():
			print("Please enter a correct filemode in octal. ")
			prusg()
			sys.exit(6)

		filepath = str(sys.argv[2])
		if not path(filepath).exists():
			print("No such file exists. Try again. ")
			prusg()
			sys.exit(7)

		if "8" in perms or "9" in perms:
			print("Enter a correct octal filemode. ")
			prusg()
			sys.exit(8)

		try:
			perms = int(perms, 8)
		except ValueError:
			print("Did you enter a correct octal number? ")
			prusg()
			sys.exit(8)


		os.chmod(filepath, perms)


def prusg():
	print("perms.py <filemode> <filepath> | example: perms.py 0644 /usr/bin/perms.py")


if __name__ == "__main__":
	main()