# __Sharif CTF 8__ 
## _fHash_

## Information
**Category:** | **Points:** | **Writeup Author**
--- | --- | ---
Crypto | 200 | MiKHalyCH

**Description:** 

> We designed a hash function called "fHash". fHash takes a message (`M`), as well as two initialization values, designated as left (`hl`) and right (`hr`). You can find the implementation of fHash [here](fHash.py).
Let `M1 = '7368617269666374'`. Notice that `fHash('7575', 'A8A8', M1) = '260c01da'`.
Find `M2 ≠ M1`, as well as two initialization values `hl` and `hr`, such that `fHash(hl, hr, M2) = '260c01da'`. That is, find a [second-preimage](https://en.wikipedia.org/wiki/Preimage_attack) for `M1`.
Each of `hl` and `hr` must be two bytes, while `M2` must be 8 bytes.

## Solution

As we can see, [algo](fHash.py) splits M1 into 4 blocks. 
We don't need to search values for all 4 iterations. Only for first. 

Now our task in searching new `hl_, hr_, m` that gives same value at first iteration, as initial `hl, hr, M1[:4]`.
It's easy to use [bruteforce](solver.py) here, because we just need to get same `md5(hr_+m)[:4]`, not full collision.
Then we can brute `hl_` and get new values for old hash: `hl_, hr_, m+M1[4:]`

