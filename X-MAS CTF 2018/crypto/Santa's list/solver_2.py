from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long
from gmpy2 import iroot
from math import log

ADDR = "199.247.6.180", 16002
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

def get_N():
    while True:
        try:
            rc = RemoteConnections(ADDR)
            res1 = rc.decrypt(pow(rc.ct, 3))
            res2 = rc.decrypt(pow(rc.ct, 3)*pow(2, e))
            if res1*2 != res2:
                N = 2*res1 - res2
                return rc, N
            rc.close()
        except Exception as ex:
            print(ex)
            continue

def decrypt_flag(rc, e, N, i):
    print 'Step {}/{}'.format(str(i).zfill(3), l)
    ct = pow(rc.ct, 2) * pow(2, i*e, N)
    res = rc.decrypt(ct % N)
    if res is not None:
        res = (res + N) // pow(2, i, N)
        return long_to_bytes(iroot(res, 2)[0])

def get_flag(flag, e, N, i):
    return (flag + N) // pow(2, i, N)

if __name__ == "__main__":
    e = 65537
    l = 710
    
    for i in range(272, l):
        rc, N = get_N()
        flag = decrypt_flag(rc, e, N, i)
        if flag:
            break
        rc.close()
    
    print 'Flag is {}'.format(flag)