from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long
from gmpy2 import iroot
from math import log

ADDR = "95.179.163.167", 16001
LOG_N = 1024

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

def RSA_LSB_PO(rc, e, N):
    l = int(log(N))
    LB, UB = 0, N

    for i in range(1, l):
        print 'Step {}/{}'.format(str(i).zfill(3), l)
        ct = pow(rc.ct, 2) * pow(2, i*e, N)
        res = rc.decrypt(ct % N)
        if res is None or not (res%2):
            UB = (UB + LB)//2
        else:
            LB = (UB + LB)//2

    return long_to_bytes(iroot(UB, 2)[0]).decode()

if __name__ == "__main__":
    e = 65537

    while True:
        rc = RemoteConnections(ADDR)
        res1 = rc.decrypt(pow(rc.ct, 3))
        res2 = rc.decrypt(pow(rc.ct, 3)*pow(2, e))
        if res1*2 != res2:
            N = 2*res1 - res2
            break
        rc.close()
    print 'Found N: {}'.format(N)
    print 'Flag is {}'.format(RSA_LSB_PO(rc, e, N))