#!/usr/bin/env python

"""https://adventofcode.com/2020/day/17."""

from itertools import chain
import os


def iter_neighbors(cube, include=False):
    adj = (-1, 0, 1)

    for x in adj:
        for y in adj:
            for z in adj:
                if not include and x == y == z == 0:
                    continue
                yield (cube[0] + x, cube[1] + y, cube[2] + z)


def iter_neighbors_w(cube, include=False):
    adj = (-1, 0, 1)

    for x in adj:
        for y in adj:
            for z in adj:
                for w in adj:
                    if not include and x == y == z == w == 0:
                        continue
                    yield (cube[0] + x, cube[1] + y, cube[2] + z, cube[3] + w)


def do_loops(loops, dimensions, iterfunc):
    grid = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[(x, y) + (0,) * (dimensions - 2)] = True if c == "#" else False

    for i in range(loops):
        changes = {}
        visited = set()
        for cube, active in grid.items():
            for c in iterfunc(cube, include=True):
                if c in visited:
                    continue
                count = 0
                for neighbor in iterfunc(c):
                    count += 1 if grid.get(neighbor) else 0
                changes[neighbor] = count in {2, 3} if grid.get(c) else count == 3
                visited.add(c)
        for k, v in changes.items():
            grid[k] = v

    return grid


if __name__ == "__main__":
    with open(os.path.join("input", "17.txt")) as f:
        lines = f.read().splitlines()

    grid = do_loops(6, 3, iter_neighbors)
    print(f"Part 1: {len([v for v in grid.values() if v])}")

    grid = do_loops(6, 4, iter_neighbors_w)
    print(f"Part 2: {len([v for v in grid.values() if v])}")
