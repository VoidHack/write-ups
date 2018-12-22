# __X-MAS CTF 2018__
## _Santa's list_

## Information
**Category:** | **Points:** | **Writeup Author**
--- | --- | ---
Crypto | 292 | MiKHalyCH

**Description:** 

> Santa's database got corrupted and now he doesn't know who was nice anymore... Can you help him find out if Galf was nice?
>
>Server: nc 199.247.6.180 16001
>
>[santas_list.zip](src/santas_list.zip) 
>
>Author: SoulTaku

## Solution
Every connection creates new `rsa = RSA.generate(1024)`. `N` is 1024 bits length (that is unknown), `e = 0x10001`.

We can encrypt everything. But our message would be added to `used` list (that contains flag from start).

Also we can decrypt everything, which result isn't devisible by elements of `used`. So we can't decrypt `flag` as it is.

Let's define `ct = E(flag) = (flag ** e) % N`.

And we need to undestand some RSA properties:
```py
D(ct**k) =
= (ct**k)**d % N =
= (ct**d)**k % N =
= (ct**d % N)**k % N =
= ((flag**e)**d % N)**k % N =
= (flag**(e**d) % N)**k % N =
= (flag % N)**k % N =
= flag**k % N
```

```py
D(ct*(i**e)) =
= ct*(i**e)**d % N =
= (flag**e)*(i**e)**d % N =
= ((flag*i)**e)**d % N =
= (flag*i)*(e**d) % N =
= flag*i % N
```

Firstly we need to find `N`. I notice that `flag**2 < N < flag**3`. It was the good idea to calculate `N`:

```py
while True:
    <create new session>
    m1 = D(ct**3)
    m2 = D(ct**3 * 2**e)
    if 2*m1 != m2:
        N = 2*m1 - m2
        break
```
How it works?
```py
(2*m1 != m2) % N => 2*m1 = m2 + N => N = 2*m1 - m2
```

Now we can encrypt messages by client side. How to find the flag? From fact that we can decrypt, I thought about Oracle Attack and found an interesting question about [RSA Least Significant Bit Padding Oracle](https://crypto.stackexchange.com/questions/11053/rsa-least-significant-bit-oracle-attack) on crypto.stackexchange.com. 

Let's define bounds at the start of algorithm:
```py
LowerBound = 0
UpperBound = N
```
In this attack we are trying to bring closer the bounds to our secret message.

At the first try we will send to decrypt `ct*(2**e)` and recieve `m' = m*2 % N -> m*2 = m' + k*N`.

* If `m'` is even, then `m*2 < N`. We need to reduce `UB`.
* If `m'` is odd, then `m*2 > N`. We need to increase `LB`.

We need to do this `log_2(N)` times increasing the multiplier twice each step.

To reduce the final bounds' size of `flag`, I've used `flag**2` and `iroot` then.

This is my interpretation of RSA LSB PO:
```py
l = log_2(N)
LB, UB = 0, N

for i in range(1, l):
    ct = (pow(ct, 2) * pow(2, i*e, N)) % N
    m = D(ct)
    if m is None or not (m % 2):
        UB = (UB + LB)//2
    else:
        LB = (UB + LB)//2

flag = iroot(UB, 2)
```

My final solution is [here](solver.py)! And it works well!

___________
## _Santa's list 2.0_

## Information
**Category:** | **Points:** | **Writeup Author**
--- | --- | ---
Crypto | 333 | MiKHalyCH, a1exdandy

**Description:** 
>Santa's MechaGnomes caught up to some intense traffic on their servers so they decided to modify santa's database server to be DDoS-proof but it still is corrupted, find out if Galf was nice or not but try not to DDoS the server.
>
>Server: nc 199.247.6.180 16002 
>
>[list_2.py](src/list_2.py)
>
>Author: SoulTaku

## Solution
This task looks same, but we can encrypt/decrypt just 5 times per one connection. 

We know that we can calculate `N` just in 2 requests. 3 left for flag RSA LSB PO. But this attack works only if we use same `N`. This time we need to create new solution!

My idea was simple. If we can find `k`: `flag**(k-1) < N` and `flag**k > N` then we can calculate `flag`:
```py
flag * 2**k % N = m' % N
flag * 2**k = m' + N
flag = (m' + N) // 2**k
```

To find `k` faster  we can use `flag**2` and then take square root of it.

Here is my [solution](solver_2.py) for second task.

## P.S.
_SoulTaku_ said that there is solution that uses only 2 requests to server. And _a1exdandy_ found an intersting [idea](solver_2_fast.py) for it.

Firstly he collects 2 pairs of `(flag**3, N)`:
```py
ns  = []
m3s = []

while len(ns) < 2:
    <create new session>
    m1 = D(ct**3)
    m2 = D(ct**3 * 2**e)
    if 2*m1 != m2:
        N = 2*m1 - m2
        ns.append(N)
        m3s.append(m1)
```

At the second step he uses [Chinese remainder theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem) to the real value of `flag**3` without modulus.