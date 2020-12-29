#!/usr/bin/env python

"""https://adventofcode.com/2015/day/02."""

from functools import reduce
from itertools import combinations
from operator import mul
import os

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "02.txt")) as f:
        lines = f.read().splitlines()

    dimensions = [sorted(int(d) for d in line.split("x")) for line in lines]

    paper = 0
    for d in dimensions:
        paper += sum(reduce(mul, combo, 2) for combo in combinations(d, 2)) + (d[0] * d[1])

    print(f"Part 1: {paper}")

    ribbons = 0
    for d in dimensions:
        ribbons += (sum(d[:-1]) * 2) + reduce(mul, d, 1)

    print(f"Part 2: {ribbons}")
