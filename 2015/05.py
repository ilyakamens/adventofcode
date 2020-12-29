#!/usr/bin/env python

"""https://adventofcode.com/2015/day/05."""

from functools import reduce
import re
import os


def is_nice_part_one(s):
    if any(pair in s for pair in ["ab", "cd", "pq", "xy"]):
        return False

    return re.match(r".*(\w)\1.*", s) and len(re.findall("[aeiou]", s)) >= 3


def is_nice_part_two(s):
    return re.match(r".*(\w{2}).*\1.*", s) and re.match(r".*(\w)\w\1.*", s)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "05.txt")) as f:
        lines = f.read().splitlines()

    for i, is_nice in enumerate((is_nice_part_one, is_nice_part_two), start=1):
        print(f"Part {i}: {sum(1 for l in lines if is_nice(l))}")
