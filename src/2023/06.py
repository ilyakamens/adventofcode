#!/usr/bin/env python

"""https://adventofcode.com/2023/day/06."""

from os.path import abspath, dirname, join
import math
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))


def p1(lines):
    times = map(int, re.findall(r"(\d+)", lines[0]))
    distances = map(int, re.findall(r"(\d+)", lines[1]))

    counts = []
    for t, d in zip(times, distances):
        counts.append(sum(1 if i * (t - i) > d else 0 for i in range(t)))

    return math.prod(counts)


def p2(lines):
    time = int("".join(re.findall(r"(\d+)", lines[0])))
    distance = int("".join(re.findall(r"(\d+)", lines[1])))

    return sum(1 if i * (time - i) > distance else 0 for i in range(time))


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "06.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
