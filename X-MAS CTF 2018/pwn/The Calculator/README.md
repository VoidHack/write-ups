# __X-MAS CTF 2018__
## _The Calculator_

## Information
**Category:** | **Points:** | **Writeup Author**
--- | --- | ---
Pwn | 495 | a1exdandy

**Description:** 

>Here is some strange calculator that is used by Elves, but it seems very poorly implemented. Could you take a look if it is secure?
>
>Download [chall](files/part1/chall)
>
>Running on: nc 199.247.6.180 10008
>
>Author: littlewho

## Solution

We have binary with format-string vulnerability, but input restircted for only `%n` and modifications (`%N$n`, `%N$hn` and so on for some integer `N`).
Also, we have calculator with operation `+`, `-`, `<`, `=`, `>`, `#` (put value to `register1`), `$` (put value to `register2`), `@` (get value of `register2`), `!` (get value of `register1`). We can distinguish value `0` and `1` of result, other values are indistinguishable (`Santa hates those big numbers...`).
We can put some complex expressions, e.g. `1 + 2 + 3 + 4`, and all intermediate calculations will be on stack after that.
Also, `register2` contains buffer address at startup. So, we can put non-zero value at `buffer[31]` to leak flag.

Final solution is:

```
@+31 %9$hhn
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

![solution](images/part1.png)

## _The Calculator 2.0_

## Information
**Category:** | **Points:** | **Writeup Author**
--- | --- | ---
Crypto | 497 | a1exdandy

**Description:** 

>I know you pwned it last time, but it was too easy. Could you give it another shot?
>
>Download [chall](files/part2/chall)
>
>Running on: nc 199.247.6.180 10009
>
>Author: littlewho

## Solution

Now, we can't use `register2` in our calculations. But we can comapre it with `<`, `=`, `>`, so, with binary search we can found buffer address and then use same method as in first part. But, we can't use 64-bit register directly. So, firslty we load constant part of 64-bit buffer address in `register1`, then compare `register2` with `register1` + `some interesting value`.

To put constant part of buffer address in register I use next expressions:
```
2147221504 + 2147221504 #
!+!+!+!+!+!+!+!#
!+!+!+!+!+!+!+!#
!+!+!+!+!+!+!+!#
!+!+!+!+!+!+!+!#
!+!+!+!+!+!+!+!#
```

After this expressions we have value `0x7ffc00000000` in `register1`. Then we chack if `register2` in bound `[register1 + 0, register2 + MAX_INT]` and if true, we can find buffer address with binary search (let's it be `X`). After that, to put non-zero value at buffer[31], we can use `!+X+31 %%10$hhn`

[Final solution](files/satanic_calculator_pt2.py)

>Ave Satani! <3
