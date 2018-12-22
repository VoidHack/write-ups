# Let's Crack the Greater lapland monolith (465 PTS)

### Description

>"Hey, do you remember that monolith I had to get in last week? Now I stumbled upon something greater and shinier! Can you help me get access to this one?" ~ The same shady dealer gnome
>
>_Authors: Milkdrop + Gabies_

Links:
- Server: [http://199.247.6.180:12006](http://199.247.6.180:12006)

Flag: ```X-MAS{Bru73_F0rc3_1s_gr34t_bu7_LCG_1s_b3tt3r___}```

### Solution

#### This challenge has the first part. You might want to read [the previous writeup](../Let%27s%20Crack%20the%20Great%20lapland%20monolith/README.md).

<p><img src='images/website.jpg' /></p>

Website contains a single input, holds `PHPSESSID` cookie, and we need to get _guess streak_ again. 

But, unfortunately, Monolith periodically changes his mind (every 100 guesses). This is the only difference with previous version of the challenge, but we can't use the same method again.

<p><img src='images/changed.jpg' /></p>

After solving the first part of the challenge, we know the type of used random generator: it's [LCG](https://en.wikipedia.org/wiki/Linear_congruential_generator). So that's a time to solve the challenge by an intended way!

Linear congruential generator can be represent by a recurrence relation

```
Xn = (A * Xn-1 + B) mod M
```

Where:
- A is multiplier
- B is increment
- M is modulus

So we need to recover these three components to perform a prediction of next generated numbers.

After some searching I've found [an article](https://tailcall.net/blog/cracking-randomness-lcgs/) describes an attack to LCG's. I used parts of `python` code from the article and wrote [solver.py](solver.py). It works insanely fast, because it needs only 10 numbers instead of all period.

```sh
$ python3 solver.py 
modulus=56263, multiplier=6620, increment=38763
X-MAS{Bru73_F0rc3_1s_gr34t_bu7_LCG_1s_b3tt3r___}
```

<p><img src='images/flag.jpg' /></p>
