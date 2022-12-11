#!/usr/bin/env python

"""https://adventofcode.com/2022/day/08."""

from collections import *
from os.path import abspath, dirname, join
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from utils import *


def is_visible(x, y, tree, rows, cols):
    col = cols[y]
    row = rows[x]
    l, r = col[:x], col[x + 1 :]
    d, u = row[:y], row[y + 1 :]

    return (
        all(tree > t for t in l)
        or all(tree > t for t in r)
        or all(tree > t for t in d)
        or all(tree > t for t in u)
    )


def p1(rows, cols):
    visible_count = 0

    for x, row in enumerate(rows):
        for y, tree in enumerate(row):
            visible_count += 1 if is_visible(x, y, tree, rows, cols) else 0

    return visible_count


def scenic_score(x, y, tree, rows, cols):
    col = cols[y]
    row = rows[x]
    l, r = col[:x], col[x + 1 :]
    u, d = row[:y], row[y + 1 :]

    scenic_score = 1
    for trees in (reversed(l), r, d, reversed(u)):
        direction_score = 0
        for t in trees:
            direction_score += 1
            if t >= tree:
                break

        scenic_score *= direction_score

    return scenic_score


def p2(rows, cols):
    max_scenic_score = 0

    for x, row in enumerate(rows):
        for y, tree in enumerate(row):
            max_scenic_score = max(
                scenic_score(x, y, tree, rows, cols), max_scenic_score
            )

    return max_scenic_score


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "08.txt")) as f:
        lines = f.read().splitlines()

    rows = []
    cols = [[] for _ in range(len(lines[0]))]
    for i, line in enumerate(lines):
        row = []
        for j, t in enumerate(list(line)):
            t = int(t)
            row.append(t)
            cols[j].append(t)
        rows.append(row)

    print(f"Part 1: {p1(rows, cols)}")
    print(f"Part 1: {p2(rows, cols)}")
