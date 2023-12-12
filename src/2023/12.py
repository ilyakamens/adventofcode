#!/usr/bin/env python

"""https://adventofcode.com/2023/day/12."""

import functools
from os.path import abspath, dirname, join
import sys

sys.path.append(dirname(dirname(abspath(__file__))))


@functools.cache
def calc(springs, damaged, needs, si=0, di=0, c=None):
    if si == len(springs):
        return bool(di == len(damaged) - 1 and needs == 0)

    if not c:
        c = springs[si]

    if c == "?":
        dot = calc(springs, damaged, needs, si, di, c=".")
        hash = calc(springs, damaged, needs, si, di, c="#")
        return dot + hash

    if c == ".":
        if 0 < needs < damaged[di]:
            return 0
        if needs == 0 and di < len(damaged) - 1:
            di += 1
            needs = damaged[di]

    if c == "#":
        if needs == 0:
            return 0
        needs -= 1

    return calc(springs, damaged, needs, si + 1, di)


def p1(lines):
    sums = 0

    for line in lines:
        springs, damaged = line.split(" ")
        damaged = tuple([int(n) for n in damaged.split(",")])

        sums += calc(springs, damaged, damaged[0])

    return sums


def p2(lines):
    sums = 0

    for line in lines:
        springs, damaged = line.split(" ")
        springs = "?".join([springs] * 5)
        damaged = tuple([int(n) for n in damaged.split(",")])
        damaged = damaged * 5

        sums += calc(springs, damaged, damaged[0])

    return sums


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "12.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
