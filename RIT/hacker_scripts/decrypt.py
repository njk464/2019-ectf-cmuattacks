#!/usr/bin/env python3
import os
import sys
import argparse
import re
import subprocess
import base64
import hmac
import hashlib
import binascii
from Crypto.Cipher import AES
from Crypto.Util import Counter

def decrypt(game, key, iv):
	ctr = Counter.new(128, little_endian=False, initial_value=0)
	encryption_suite = AES.new(key, AES.MODE_CTR, counter=ctr)
	g_src = encryption_suite.decrypt(game)

	assert('ELF' in str(g_src))
	return g_src

# strip out the header
if __name__=="__main__":
	try:
		#base64 string of the key (notably KEY_1)
		key = sys.argv[1]
		#game file 
		encrypted_game_file = sys.argv[2]
	except:
		print("./decrypt.py <base64 KEY_1> <path to encrypted game>")
		return	
	f = open(encrypted_game_file, 'rb')
	#discard headers
	print(f.readline())
	print(f.readline())
	print(f.readline())
	print(f.readline())

	game = f.read()
	f.close()

	print('Decrypting...')
	decrypted = decrypt(game, base64.b64decode(key), 0)
	d_fname = 'decrypted_' + encrypted_game_file
	f = open(d_fname, 'wb')
	f.write(decrypted)
	f.close()
	print('File %s Done!' % (d_fname))
	
