#!/usr/bin/env python

"""https://adventofcode.com/2023/day/03."""

from collections import defaultdict
import math
from os.path import abspath, dirname, join
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

MAPPING = defaultdict(list)


def find_digits(schematic):
    for i, line in enumerate(schematic):
        for match in re.finditer(r"\d+", line):
            yield i, match


def iter_surrounding(i, start, end, schematic):
    if start > 0:
        start -= 1
    if end == len(schematic[i]):
        end -= 1

    for x in [i - 1, i, i + 1]:
        if x >= 0 and x < len(schematic):
            yield x, start, end


def has_symbol(s):
    return re.search(r"[^\d\.]", s) is not None


def is_adjacent(i, start, end, schematic):
    for x, start, end in iter_surrounding(i, start, end, schematic):
        if has_symbol(schematic[x][start : end + 1]):
            return True


def star_coords(s):
    return [m.span() for m in re.finditer(r"\*", s)]


def get_stars(i, start, end, num, schematic):
    for x, start, end in iter_surrounding(i, start, end, schematic):
        for l, _ in star_coords(schematic[x][start : end + 1]):
            MAPPING[(x, l + start)].append(num)


def p1(schematic):
    sums = 0

    for i, m in find_digits(schematic):
        if is_adjacent(i, *m.span(), lines):
            sums += int(m.group())

    return sums


def p2(schematic):
    for i, m in find_digits(schematic):
        get_stars(i, *m.span(), int(m.group()), lines)

    return sum([math.prod(nums) for nums in MAPPING.values() if len(nums) == 2])


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "03.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
