# __X-MAS CTF 2018__ 
## _Santa's Secret B(i)smuth_

## Information
**Category:** | **Points:** | **Writeup Author**
--- | --- | ---
Crypto | 499 | MiKHalyCH

**Description:** 

> Samba's Union have found some of Santa's ancient and most valuable secrets. Luckily, they are encrypted, even so, you must be quick enough to retrieve them before the Sambas do!
>
>Sadly, Santa does not remember the encryption scheme, he does remember though that it had something to do with bismuth, or was it something else...?
>
>[flag.enc](src/flag.enc)
>
>Author: Gabies

## Solution
According to crypto tasks experience it was realy easy to understand that it is some secret sharing system. But it took a lot of time to find the right name of it.

One realy good step was googling [secret sharing smuth](http://lmgtfy.com/?q=secret+sharing+smuth).

This is [Asmuth-Bloom's threshold secret sharing scheme](http://cryptowiki.net/index.php?title=Asmuth-Bloom_scheme):

```py
common_part = p
Secret = [(I_i, p_i) for i in range(10)]
```

[Solution](solver.py) can be easily found by [Chinese remainder theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem).

