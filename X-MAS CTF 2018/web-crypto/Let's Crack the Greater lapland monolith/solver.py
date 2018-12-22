#!/usr/bin/python3

import re
import requests

from gmpy2 import gcd, invert
from functools import reduce


url = 'http://199.247.6.180:12006/?guess={}'
recover_size = 10
streak_count = 20


class LCG:
    def __init__(self, m, a, c, seed):
        self.m = m
        self.a = a
        self.c = c
        self.state = seed

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state


def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment


def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * invert(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)


def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return crack_unknown_multiplier(states, modulus)


def recover_lcg(session):
    numbers = []
    for i in range(recover_size):
        html = session.get(url.format(1)).text
        number = int(re.search('<br>(\d+)<br>', html).group(1))
        numbers.append(number)
    modulus, multiplier, increment = crack_unknown_modulus(numbers)
    lcg = LCG(modulus, multiplier, increment, numbers[-1])
    return lcg


def obtain_flag(lcg, session):
    numbers = [lcg.next() for i in range(streak_count)]
    for number in numbers:
        html = session.get(url.format(number)).text
        match = re.search('X-MAS\{.*?\}', html)
        if match:
            return match.group(0)


if __name__ == '__main__':
    session = requests.session()
    lcg = recover_lcg(session)
    print('modulus={}, multiplier={}, increment={}'.format(lcg.m, lcg.a, lcg.c))
    flag = obtain_flag(lcg, session)
    print(flag)
