#!/usr/bin/python

import sys
import gmpy2
import requests

from hashlib import sha512, md5, sha1, sha384, sha224, sha256
from itertools import product
from string import digits, ascii_lowercase

from pwn import *
from Crypto.Util.number import *


def brute(io):
    line = io.readline()
    end = line[-7:-1]
    if 'md5' in line:
        func = md5 
    if 'sha512' in line:
        func = sha512
    if 'sha1' in line:
        func = sha1
    if 'sha384' in line:
        func = sha384
    if 'sha224' in line:
        func = sha224
    if 'sha256' in line:
        func = sha256
    for length in range(1, 10):
        for x in product(digits+ascii_lowercase, repeat=length):
            x = ''.join(x)
            h = func(x.encode('utf8')).hexdigest()
            if h[-6:] == end:
                return x


def bypass(io):
    io.recvuntil('Submit')
    io.sendline(brute(io))



def solve(r, n, e, c):
    nn = n * n
    r_e = pow(r, e, nn)
    c = (c * gmpy2.invert(r_e, nn)) % nn
    m = ((c - r ** 2) % nn) // n
    return m

def crack_r(p, n, e, c):
    q = n // p
    phi = (p-1)*(q-1)
    d = inverse(e+2, phi)
    s = c % n
    return pow(s, d, n)


def continue_strange(io, p, n, c):
    e = 0x10001
    print("Founded:")
    print(p, n, c)
    r = crack_r(p, n, e, c)
    m = solve(r, n, e, c)
    m = long_to_bytes(m)
    print(m)
    io.sendline('S')
    io.sendline(m)
    io.interactive()


def strange_brute(addr, url_mask):
    while True:
        try:
            io = remote(*addr)
            bypass(io)
            io.sendline('P')
            io.recvuntil('65537, ')
            n = int(io.readline()[:-3])
            print("N:", n)
            io.sendline("C")
            io.recvuntil("enc = ")
            c = int(io.readline().strip())
            print("C:", c)
            ans = requests.get(url_mask.format(str(n))).text
            print(ans)
            if 'p=' in ans:
                p = int(ans.split('=')[1])
                continue_strange(io, p, n, c)
            io.close()
        except KeyboardInterrupt:
            break


def main(addr):
    io = remote(*addr)
    bypass(io)
    io.interactive()


if __name__ == '__main__':
    addr = '37.139.4.247', 36032
    url_mask = 'http://<server>/check/{0}/'
    # main(addr)
    strange_brute(addr, url_mask)