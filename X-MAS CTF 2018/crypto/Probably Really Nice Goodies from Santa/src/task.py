import os

flag = open('flag.txt').read().strip()

class PRNG():
	def __init__(self):
		self.seed = self.getseed()
		self.iv = int(bin(self.seed)[2:].zfill(64)[0:32], 2)
		self.key = int(bin(self.seed)[2:].zfill(64)[32:64], 2)
		self.mask = int(bin(self.seed)[2:].zfill(64)[64:96], 2)
		self.aux = 0

	def parity(self,x):
		x ^= x >> 16
		x ^= x >> 8
		x ^= x>> 4
		x ^= x>> 2
		x ^= x>> 1
		return x & 1
	
	def getseed(self):
		return int(os.urandom(12).encode('hex'), 16)
	
	def LFSR(self):
		return self.iv >> 1 | (self.parity(self.iv&self.key) << 32)
	
	def next(self):
		self.aux, self.iv = self.iv, self.LFSR()
	
	def next_byte(self):
		x = self.iv ^ self.mask
		self.next()
		x ^= x >> 16
		x ^= x >> 8
		return (x & 255)

def encrypt(s):
	o=''
	for x in s:
		o += chr(ord(x) ^ p.next_byte())
	return o.encode('hex')

p=PRNG()

with open('flag.enc','w') as f:
	f.write(encrypt(flag))
