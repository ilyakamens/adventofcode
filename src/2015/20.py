#!/usr/bin/env python

"""https://adventofcode.com/2015/day/20."""

from main import main, runs
from utils import divisors


def presents(n: int) -> int:
    ds = sum(divisors(n))

    return ds * 10


def presents2(n: int) -> int:
    ds = sum(d for d in divisors(n) if n / d <= 50)

    return ds * 11


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    n = 1
    while presents(n) < int(input):
        n += 1

    return n


@runs(cases={'1'})
def p2(input: str, case: str) -> int:
    n = 1
    while presents2(n) < int(input):
        n += 1

    return n


if __name__ == '__main__':
    main(p1, p2, [6], [6])
