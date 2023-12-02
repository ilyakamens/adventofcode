#!/usr/bin/env python

"""https://adventofcode.com/2023/day/02."""

from collections import defaultdict
import math
from os.path import abspath, dirname, join
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

COLORS = dict(red=12, green=13, blue=14)
REGEX = r"(\d+) (%s)" % "|".join(COLORS.keys())


def p1(lines):
    sum = 0
    for line in lines:
        l, r = line.split(":")
        game = int(l.split(" ")[1])

        matches = re.findall(REGEX, r)
        for num, color in matches:
            if int(num) > COLORS[color]:
                break
        else:
            sum += game

    return sum


def p2(lines):
    sum = 0
    for line in lines:
        counts = defaultdict(int)

        matches = re.findall(REGEX, line)
        for num, color in matches:
            counts[color] = max(int(num), counts[color])

        sum += math.prod(counts.values())

    return sum


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "02.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
