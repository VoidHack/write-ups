# ASIS CTF Finals 2018 
## Ariogen

## Information
**Category:** | **Points:** | **Writeup Author**
--- | --- | ---
Crypto | 273 | MiKHalyCH, keltecc

**Description:** 

> looks a bit weird? let's have a crack at it!
`nc 37.139.4.247 36032`

## Solution
We have two functions:
```py
def makekey(nbit):
    fprime = gmpy2.next_prime(2 ** nbit)
    D = getRandomRange(1, nbit**3)
    p = gmpy2.next_prime(fprime + D)
    q = getPrime(nbit)
    pubkey = (0x10001, int(p*q)) 
    return p, pubkey

def encrypt(m, pubkey):
    m = bytes_to_long(m)
    e, n = pubkey
    assert m < n
    while True:
        r = random.randint(1, n - 1)
        if gmpy2.gcd(r, n) == 1:
            c = (pow(r, e, n**2) * (r**2 + m*n)) % n ** 2   
            break
    return r, c
```
Also we have `e, n = pubkey, c = enc`.

### First step

Firstly we need to understand, how to reverse crypto algorythm. We can try to make it step by step:

```py
n_2 = n*n
r_e = pow(r, e, n**2)


c = r_e * (r**2 + m*n)) % n_2
c * inverse(r_e, n**2) % n_2 = (r**2 + m*n)) # beacuse right part is always lower then n_2
(c * inverse(r_e, n**2) - r**2) % n_2 = m*n
((c * inverse(r_e, n**2) - r**2) % n_2) // n = m
```
To solve this equation we should know `r`. Is there any way to find it???

### Second step

So lets rearrange `c`:
```
c = (r**e * (r**2 + m*n)) % n**2
c = (r**e * (r**2) + (m * n * r**e) % n**2
c = (r**(e+2) + (m * n * r**e)) % n**2
```

From this equation we can understand that `c % n = (r**(e+2) + (m * n * r**e)) % n = r ** (e+2) % n`. Left part can be easy calculated. But what about right part???

### Third step

`pow(r, e+2, n) = c % n` looks like the classic RSA: `pow(m, e, N) = c`.

To decrypt it, we need to know private key `d`: `m = pow(c, d, N)`.

`d = inverse(e, phi) = inverse(e, (p-1)*(q-1))`. 

Now we need to find factorisation of `n`. Let's look at `makekey` function:

```py
fprime = gmpy2.next_prime(2 ** nbit)
D = getRandomRange(1, nbit**3)
p = gmpy2.next_prime(fprime + D)
```
This code makes it clear that `p` factors of all `N's` are close to each other, because `D` is too low in comparison with `fprime`.

We can try to collect a database of generated pubkeys and calculate `gcd` of current and old `N's`. If `gcd(cur_N, old_N) != 1` than it would be equal to `p`. After that we can factorise `N` and calculate `r`:

```py
d = inverse(e+2, (p-1)*(q-1))
r = pow(c % n, d, n)
```

### Fourth step

To solve this task we launched our server on the remote host. It accepted requests with new `N` and checked `gcd` with old ones. 

This server helped us to collect `N's` from different hosts.

Our [solver](solver.py) sent to our server new `N` and if his `gcd` calculated valid `p`, it started to decrypt message with algo from [First step](#first-step). After sending of right decrypted message, task server sent back the flag.