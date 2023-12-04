#!/usr/bin/env python

"""https://adventofcode.com/2023/day/04."""

from os.path import abspath, dirname, join
import math
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))


def iter_cards(lines):
    for line in lines:
        winning, mine = line.split(": ")[1].split(" | ")
        winning = set(re.findall(r"(\d+)", winning))
        mine = set(re.findall(r"(\d+)", mine))

        yield len(winning & mine)


def p1(lines):
    sums = 0
    for count in iter_cards(lines):
        sums += math.pow(2, count - 1) if count else 0

    return int(sums)


def p2(lines):
    counts = [1] * len(lines)

    for i, count in enumerate(iter_cards(lines)):
        for j in range(i + 1, i + count + 1):
            counts[j] += counts[i]

    return sum(counts)


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "04.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
