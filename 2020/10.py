#!/usr/bin/env python

"""https://adventofcode.com/2020/day/10."""

from collections import defaultdict
import os
import re

cache = {}


def tribonacci(n):
    if n == 0:
        return 0
    if n in {1, 2}:
        return 1
    if n not in cache:
        cache[n] = tribonacci(n - 3) + tribonacci(n - 2) + tribonacci(n - 1)

    return cache[n]


if __name__ == "__main__":
    with open(os.path.join("input", "10.txt")) as f:
        jolts = sorted([0] + [int(line) for line in f.read().splitlines()])
        jolts.append(jolts[-1] + 3)

    diffs = defaultdict(int)
    difflist = []
    for i, jolt in enumerate(jolts[1:], start=1):
        diff = str(jolt - jolts[i - 1])
        diffs[diff] += 1
        difflist.append(diff)

    print(f"Part 1: {diffs['1'] * diffs['3']}")

    permutations = 1
    for group in re.findall("[1]{2,}", "".join(difflist)):
        permutations *= tribonacci(len(group) + 1)

    print(f"Part 2: {permutations}")
