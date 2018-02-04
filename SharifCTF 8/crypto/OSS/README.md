# __Sharif CTF 8__ 
## _OSS_

## Information
**Category:** | **Points:** | **Writeup Author**
--- | --- | ---
Crypto | 100 | MiKHalyCH

**Description:** 

> In this question, you are asked to generate an OSS (Ong-Schnorr-Shamir) signature on some message, given a pair of known signatures. Further description can be found [here](pdfs/OSS_Signature.pdf).
You can verify the validity of your signature using [this Python script](verify.py) locally, prior to submitting it here. Upon submitting a valid signature, you'll receive the flag.

## Solution

We have `m1` and `m2`, need to found `m1 * m2`
It means, that we can use [Pollard’s Solution of OSS Equations](pdfs/Pollard.pdf) (122 page)

```py
m = (m1*m2) % n
s1 = (x1*x2 + k*y1*y2) % n
s2 = (x1*y2 - x2*y1) % n

print(verify(public, m2, (s1, s2)))
```