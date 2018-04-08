import gmpy2
gmpy2.get_context().precision = 4096
from binascii import unhexlify
from functools import reduce
from gmpy2 import root
from itertools import permutations
from Crypto.Util.number import long_to_bytes

# Håstad's Broadcast Attack
# https://id0-rsa.pub/problem/11/

# Resources
# https://en.wikipedia.org/wiki/Coppersmith%27s_Attack
# https://github.com/sigh/Python-Math/blob/master/ntheory.py

EXPONENT = 3

def chinese_remainder_theorem(items):
    # Determine N, the product of all n_i
    N = 1
    for a, n in items:
        N *= n

    # Find the solution (mod N)
    result = 0
    for a, n in items:
        m = N // n
        r, s, d = extended_gcd(n, m)
        if d != 1:
            raise "Input not pairwise co-prime"
        result += a * s * m

    # Make sure we return the canonical solution.
    return result % N


def extended_gcd(a, b):
    x, y = 0, 1
    lastx, lasty = 1, 0

    while b:
        a, (q, b) = b, divmod(a, b)
        x, lastx = lastx - q * x, x
        y, lasty = lasty - q * y, y

    return (lastx, lasty, a)


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1

def get_value(filename):
    with open(filename) as f:
        value = f.readline()
    return int(value, 16)

def solve(ciphertexts, modulus):
    C = chinese_remainder_theorem(list(zip(ciphertexts, modulus)))
    M = int(root(C, 3))
    M = long_to_bytes(M)
    if b'flag' in M:
        print(M.decode())
        exit()

def read_data():
    with open('ciphertexts.txt') as f:
        cts = map(lambda x: int(x.strip(), 16), f.readlines())

    with open('moduli.txt') as f:
        nss = map(lambda x: int(x.strip(), 16),f.readlines())
    
    return tuple(cts), tuple(nss)

if __name__ == "__main__":
    cts, nss = read_data()
    for c in permutations(cts,3):
        solve(c, nss)