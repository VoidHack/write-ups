#!/usr/bin/env python3
from random import randint
from base64 import b64encode

def xor(data, key):
    out = b''
    for n in range(len(data)):
        out += bytes([data[n] ^ key[n % len(key)]])
    return out

def randkey():
    key = b''
    for n in range(randint(128, 255)):
        key += bytes([randint(0, 255)])
    return key

if __name__ == "__main__":
    with open('flag', 'rb') as f:
        data = f.read()
    print(b64encode(xor(data, randkey())).decode("utf-8"))
