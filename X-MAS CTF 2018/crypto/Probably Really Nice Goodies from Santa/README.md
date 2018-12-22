# __X-MAS CTF 2018__ 
## _Probably Really Nice Goodies from Santa_

## Information
**Category:** | **Points:** | **Writeup Author** | **Solution author**
--- | --- | --- | ---
Crypto | 460 | MiKHalyCH | a1exdandy

**Description:** 

> Everybody knows that Santa loves sharing! Of course, you should Probably be Really Nice with your friends to get any Goodies from him.
>
>[goodies.zip](src/goodies.zip)
>
>Author: Gabies

## Solution

This [task](src/task.py) is about some [Pseudorandom number generator](https://en.wikipedia.org/wiki/Pseudorandom_number_generator). 

Firstly let's rewrite `PRNG` class from task to make it z3-compatible.

We know that flag starts with `X-MAS{` and ends with `}`. The length of flag is equal to length of ciphertext. This fact helps us to start solving our z3 model. 

Let's start to brute the first unknown symbol of flag:
```py
for c in string.printable.replace('?', ''):
    flag[pos] = ord(c)
    print(flag.decode())

    iv = BitVec('iv', 32)
    key = BitVec('key', 32)
    mask = BitVec('mask', 32)

    p = PRNG_z3(iv, key, mask)
    s = Solver()
    for a, b in zip(encflag, flag):
        byte = p.next_byte()
        if b != ord('?'):
            s.add(simplify(byte ^ b == a))
    res = s.check()
    if res == sat:
        break
```

It was noticed that one of charaters takes much more time to solve then others. This was the main idea of exploit!

Now we can set timeout for solver and check the time of work. If it is realy big, we can say that this is right character.

This is the full [solution](solver.py)!