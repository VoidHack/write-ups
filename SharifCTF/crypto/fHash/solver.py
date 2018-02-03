from random import choice
from fHash import foo
from itertools import permutations

hexdigits = '0123456789abcdef'
h1, h2 = 'dcd0', 'a6ea'


def choice_hr_m():
    res = ''.join(choice(hexdigits) for x in range(8))
    return res[:4], res[4:]

def brute_hl(m):
    for hl in map(''.join, permutations(hexdigits, 4)):
        if h2 == foo(hl, m):
            return hl

if __name__ == "__main__":
    while True:
        hr, m = choice_hr_m()
        if h1 == foo(hr, m):
            # print('First done:', hr, m)
            hl = brute_hl(m)
            if hl:
                print('Second done!', hr, hl, m+'617269666374')                
                break