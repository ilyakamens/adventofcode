#!/usr/bin/env python

"""https://adventofcode.com/2021/day/05."""

from collections import defaultdict
import os

def p1(lines):
    m = defaultdict(int)

    for line in lines:
        left, right = line.split(" -> ")
        x1, y1 = [int(x) for x in left.split(",")]
        x2, y2 = [int(y) for y in right.split(",")]

        if x1 != x2 and y1 != y2:
            if abs((y2 - y1) / (x2 - x1)) != 1:
                continue


            if x1 > x2:
                xstart = x2
                xend = x1
                ystart = y2
                yend = y1
            else:
                xstart = x1
                xend = x2
                ystart = y1
                yend = y2

            i = 0
            for x in range(xstart, xend + 1):
                if ystart < yend:
                    sign = 1
                else:
                    sign = -1
                m[(x, ystart + (i * sign))] += 1
                i += 1
            continue

        if x1 != x2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                assert y1 == y2
                m[(x, y1)] += 1

        if y1 != y2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                assert x1 == x2
                m[(x1, y)] += 1

    count = 0
    for n in m.values():
        if n >= 2:
            count += 1

    return count

def p2(lines):
    pass

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "05.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
