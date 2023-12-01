#!/usr/bin/env python

"""https://adventofcode.com/2023/day/01."""

import os
import re


def p1(lines):
    sum = 0

    for line in lines:
        matches = re.findall(r"\d", line)
        sum += int(f"{matches[0]}{matches[-1]}")

    return sum


def p2(lines):
    nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    mapping = {n: i for i, n in enumerate(nums, start=1)}
    rmapping = {n[::-1]: i for i, n in enumerate(nums, start=1)}
    regex = rf"(\d|{'|'.join(nums)})"
    rregex = rf"(\d|{reversed('|'.join(nums))})"

    sum = 0

    for line in lines:
        first = re.search(regex, line).group()
        last = re.search(rregex, line[::-1]).group()
        if first in mapping:
            first = mapping[first]
        if last in rmapping:
            last = rmapping[last]
        sum += int(f"{first}{last}")

    return sum


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "01.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
