from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long
from random import getrandbits
from functools import reduce
from gmpy2 import gcd, invert
from gmpy2 import iroot, mpz
from math import log


ADDR = "199.247.6.180", 16002
LOG_N = 1024


def crt(a, n):
    sum = 0
    prod = reduce(lambda x, y: x * y, n)

    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * invert(p, n_i) * p
    return sum % prod


class RemoteConnections:
    def __init__(self, addr):
        self.r = remote(*addr)
        self.r.recvuntil('Galf - ')
        self.ct = int(self.r.recvuntil('\n').strip(), 16)

    def close(self):
        self.r.close()

    def encrypt(self, m):
        self.r.sendlineafter('Exit\n', '1')
        self.r.sendlineafter('Plaintext > ', long_to_bytes(m))
        self.r.recvuntil('Encrypted: ')
        return int(self.r.recvline().strip())

    def decrypt(self, c):
        self.r.sendlineafter('Exit\n', '2')
        self.r.sendlineafter('Ciphertext > ', str(c))
        if 'Ho, ho' in self.r.recvline(): 
            return
        self.r.recvuntil('Decrypted: ')
        return int(self.r.recvline().strip())
    
    def exit(self):
        self.r.sendlineafter('Exit\n', '3')
        self.r.recvall()


if __name__ == "__main__":
    e = 65537
    
    m3s = []
    ns = []

    while len(ns) < 2:
        rc = RemoteConnections(ADDR)
        A = rc.decrypt(pow(rc.ct, 3))
        B = rc.decrypt(pow(rc.ct, 3) * pow(2, e))
        if A*2 == B:
            rc.close()
            continue
        N = A*2 - B
        ns.append(N)
        m3s.append(A)
        rc.close()

    m3 = crt(m3s, ns)
    m, _ = iroot(m3, 3)
    flag = long_to_bytes(m)
    print 'Flag is {}'.format(flag)