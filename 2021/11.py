#!/usr/bin/env python

"""https://adventofcode.com/2021/day/11."""

from collections import defaultdict
import os

def adjacent(x, y):
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            yield x + i, y + j

def print_grid(grid):
    rows = []
    for (_, y), v in grid.items():
        if len(rows) <= y:
            rows.append([])
        rows[y].append(v)

    for row in rows:
        print("".join(str(x) for x in row))

def p1(lines):
    octopi = {}
    for y, line in enumerate(lines):
        for x, o in enumerate(line):
            octopi[(x, y)] = int(o)

    flashes = 0
    for _ in range(100):
        flashed = set()
        to_increment = [pos for pos in octopi.keys()]
        while to_increment:
            pos = to_increment.pop()
            if pos in flashed:
                continue
            o = octopi.get(pos)
            if o is None:
                continue
            octopi[pos] += 1
            if octopi[pos] >= 10:
                flashes += 1
                flashed.add(pos)
                for x2, y2 in adjacent(*pos):
                    to_increment.append((x2, y2))
        for pos, o in octopi.items():
            if o >= 10:
                octopi[pos] = 0

    return flashes



def p2(lines):
    octopi = {}
    for y, line in enumerate(lines):
        for x, o in enumerate(line):
            octopi[(x, y)] = int(o)

    step = 0
    while True:
        step += 1
        flashed = set()
        to_increment = [pos for pos in octopi.keys()]
        while to_increment:
            pos = to_increment.pop()
            if pos in flashed:
                continue
            o = octopi.get(pos)
            if o is None:
                continue
            octopi[pos] += 1
            if octopi[pos] >= 10:
                flashed.add(pos)
                for x2, y2 in adjacent(*pos):
                    to_increment.append((x2, y2))
        for pos, o in octopi.items():
            if o >= 10:
                octopi[pos] = 0
        if all(o == 0 for o in octopi.values()):
            return step



if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "11.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
