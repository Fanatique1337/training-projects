
#!/usr/bin/env python

# Needed library imports

import blowfish # import the blowfish module for encryption 
from os import urandom # import urandom for vector initialization
# from pg import db # import database API for PostgreSQL (for later updates)


class TestIt(object):
	byte_order = "big"

	@classmethod
	def setUpClass(cls):
		cls.cipher = blowfish.Cipher(
			b"somekey",
			byte_order = cls.byte_order)


	def encryptit(self, word):
		cipher = self.cipher

		iv = urandom(8)

		enc = b"".join(cipher.encrypt_cfb(word, iv))
		print(enc)
		dec = b"".join(cipher.decrypt_cfb(enc, iv))
		print(dec)
		return enc

# Define the main function.

def main():

	# Initialize all variables that need to be used.
	database = []
	filepath = "pwdb.dat"

	tmpsite = input("Website the password is for: ")
	tmppassword = input("The password is: ").encode('utf-8')

	handler = TestIt()
	handler.setUpClass()
	tmppassword = handler.encryptit(tmppassword)
	seq = (tmpsite, str(tmppassword))
	database = ",".join(seq)
	with open(filepath, "wb") as fileh:
		for entry in database:
			fileh.write(entry.encode('utf-8'))
			fileh.write('\n')
	fileh.close()



if __name__ == "__main__":
	main()



