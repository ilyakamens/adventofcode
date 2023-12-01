#!/usr/bin/env python

"""https://adventofcode.com/2022/day/12."""

from collections import *
from os.path import abspath, dirname, join
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from utils import *


def p1(rows, cols):
    x = y = 0
    current = rows[x][y]
    nodes = deque()
    while current != "E":
        pass


def p2(lines):
    pass


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "12.txt")) as f:
        lines = f.read().splitlines()

    rows = []
    cols = [[] for _ in range(len(lines[0]))]
    for i, line in enumerate(lines):
        row = []
        for j, t in enumerate(list(line)):
            row.append(t)
            cols[j].append(t)
        rows.append(row)

    print(f"Part 1: {p1(rows, cols)}")
    print(f"Part 2: {p2(lines)}")
