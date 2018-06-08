#!/usr/bin/env python

import blowfish

from os import urandom


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

crypt = "Test test 1 2 3".encode('utf-8')
tester = TestIt()
tester.setUpClass()
tester.encryptit(crypt)