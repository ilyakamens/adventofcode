#!/usr/bin/env python

"""https://adventofcode.com/2021/day/09."""

from collections import defaultdict
import os
import sys

def p1(lines):
    heights = {}

    for y, line in enumerate(lines):
        for x, n in enumerate(line):
            heights[(x, y)] = int(n)

    lows = []
    for (x, y), h in heights.items():
        left = heights.get((x - 1, y), sys.maxsize)
        if left <= h:
            continue
        right = heights.get((x + 1, y), sys.maxsize)
        if right <= h:
            continue
        up = heights.get((x, y - 1), sys.maxsize)
        if up <= h:
            continue
        down = heights.get((x, y + 1), sys.maxsize)
        if down <= h:
            continue

        lows.append(h)

    return sum(low + 1 for low in lows)

def p2(lines):
    heights = {}

    for y, line in enumerate(lines):
        for x, n in enumerate(line):
            heights[(x, y)] = int(n)

    lows = []
    for (x, y), h in heights.items():
        left = heights.get((x - 1, y), sys.maxsize)
        if left <= h:
            continue
        right = heights.get((x + 1, y), sys.maxsize)
        if right <= h:
            continue
        up = heights.get((x, y - 1), sys.maxsize)
        if up <= h:
            continue
        down = heights.get((x, y + 1), sys.maxsize)
        if down <= h:
            continue

        lows.append((x, y))

    basins = []
    for low in lows:
        basin_size = 0
        queue = [low]
        seen = set()
        while queue:
            x, y = queue.pop()
            if (x, y) in seen:
                continue
            if heights[(x, y)] == 9:
                continue
            seen.add((x, y))
            basin_size += 1
            for i in [-1, 1]:
                if heights.get((x + i, y), 0) > heights[(x, y)]:
                    queue.append((x + i, y))
                if heights.get((x, y + i), 0) > heights[(x, y)]:
                    queue.append((x, y + i))

        basins.append(basin_size)

    basins = sorted(basins)[-3:]
    return basins[0] * basins[1] * basins[2]





if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "09.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
