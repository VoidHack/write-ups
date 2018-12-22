import string
import time
from binascii import hexlify, unhexlify
from z3 import *


encflag = unhexlify('ab38abdef046216128f8ea76ccfcd38a4a8649802e95f817a2fc945dc04a966d502ef1e31d0a2d')
flag = b'X-MAS{'
pos = len(flag)
while len(flag) != len(encflag) - 1:
    flag += b'?'
flag += b'}'
flag = bytearray(flag)

set_param("timeout", 10000)

class PRNG_z3():
	def __init__(self, iv, key, mask):
		self.iv = ZeroExt(1, iv)
		self.key = key
		self.mask = mask

	def parity(self,x):
		x = x ^ (x >> 16)
		x = x ^ (x >> 8)
		x = x ^ (x >> 4)
		x = x ^ (x >> 2)
		x = x ^ (x >> 1)
		return x & 1
	
	def LFSR(self):
		return LShR(self.iv, 1) | (ZeroExt(1, self.parity(Extract(31, 0, self.iv)&self.key)) << 32)
	
	def next(self):
		self.iv = self.LFSR()
	
	def next_byte(self):
		x = Extract(31, 0, self.iv) ^ self.mask
		self.next()
		x = x ^ (x >> 16)
		x = x ^ (x >> 8)
		return (x & 255)

while pos < len(flag)-1:
    for c in string.printable.replace('?', ''):
        flag[pos] = ord(c)
        print(flag.decode())

        iv = BitVec('iv', 32)
        key = BitVec('key', 32)
        mask = BitVec('mask', 32)
        p = PRNG_z3(iv, key, mask)
        s = Solver()
        for a, b in zip(encflag, flag):
            byte = p.next_byte()
            if b != ord('?'):
                s.add(simplify(byte ^ b == a))
        t0 = time.time()
        res = s.check()
        t1 = time.time()
        if res == sat or (t1 - t0) > 9.5:
            break
    pos += 1