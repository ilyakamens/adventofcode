#!/usr/bin/env python

"""https://adventofcode.com/2022/day/04."""

from collections import *
from os.path import abspath, dirname, join
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from utils import *


def iterpairs(lines):
    for pair in lines:
        l, r = pair.split(",")
        l1, h1 = map(int, l.split("-"))
        l2, h2 = map(int, r.split("-"))

        yield (l1, h1), (l2, h2)


def p1(lines):
    count = 0

    for (l1, h1), (l2, h2) in iterpairs(lines):
        count += (l1 <= l2 and h2 <= h1) or (l2 <= l1 and h1 <= h2)

    return count


def p2(lines):
    count = 0

    for (l1, h1), (l2, h2) in iterpairs(lines):
        count += l1 <= l2 <= h1 or l2 <= l1 <= h2

    return count


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "04.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
