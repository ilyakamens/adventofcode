#!/usr/bin/env python

"""https://adventofcode.com/2022/day/10."""

from collections import *
from os.path import abspath, dirname, join
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from utils import *


def iter_instructions(instructions):
    for instruction in instructions:
        if instruction == "noop":
            yield 1, 0
        else:
            yield 2, int(instruction.split(" ")[1])


def p1(instructions):
    signal_strengths = 0
    x = 1
    cycle = 0

    for ticks, inc in iter_instructions(instructions):
        for _ in range(ticks):
            cycle += 1
            if cycle in {20, 60, 100, 140, 180, 220}:
                signal_strengths += cycle * x

        x += inc

    return signal_strengths


def p2(instructions):
    x = 1
    cycle = 0
    rows = []
    row = []

    for ticks, inc in iter_instructions(instructions):
        for _ in range(ticks):
            cycle += 1

            if x - 1 <= (cycle - (40 * len(rows))) - 1 <= x + 1:
                row.append("#")
            else:
                row.append(".")

            if len(row) == 40:
                rows.append(row)
                row = []

        x += inc

    return "\n" + "\n".join(["".join(row) for row in rows])


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "10.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
