# __CTF name__ 
## _task name_

## Information
**Category:** | **Points:** | **Writeup Author**
--- | --- | ---
Crypto | 200 | MiKHalyCH

**Description:** 

> sorry wrong chat
<br>e = 3 btw
<br>[ciphertexts.txt](ciphertexts.txt)  [moduli.txt](moduli.txt)

## Solution
We have 3 `N's` and 15 `C's`. We need to find only 3 `C` for classical [Hastad attack](https://en.wikipedia.org/wiki/Coppersmith%27s_attack#H%C3%A5stad's_broadcast_attack) (code from [here](https://github.com/aaossa/Computer-Security-Algorithms/blob/master/11%20-%20H%C3%A5stad's%20Broadcast%20Attack/hastads-broadcast-attack.py))

So we can [try all permutations](solver.py) to find needed pairs of `(C,N)` and crack it.
