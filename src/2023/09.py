#!/usr/bin/env python

"""https://adventofcode.com/2023/day/09."""

from os.path import abspath, dirname, join
import sys

sys.path.append(dirname(dirname(abspath(__file__))))


def calc_next(nums, i=-1, sign=1):
    if len(set(nums)) == 1:
        return nums[0]

    new = []
    for j, n in enumerate(nums[1:], start=1):
        new.append(n - nums[j - 1])

    return nums[i] + (calc_next(new, i, sign) * sign)


def p1(lines):
    sums = 0
    for line in lines:
        sums += calc_next([int(n) for n in line.split(" ")])

    return sums


def p2(lines):
    sums = 0
    for line in lines:
        sums += calc_next([int(n) for n in line.split(" ")], i=0, sign=-1)

    return sums


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "09.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
