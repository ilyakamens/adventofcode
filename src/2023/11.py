#!/usr/bin/env python

"""https://adventofcode.com/2023/day/11."""

from os.path import abspath, dirname, join
import sys

sys.path.append(dirname(dirname(abspath(__file__))))


def get_empties(lines):
    ys = []
    for y, line in enumerate(lines):
        if all(c == "." for c in line):
            ys.append(y)

    xs = []
    for x in range(len(lines[0])):
        if all(lines[y][x] == "." for y in range(len(lines))):
            xs.append(x)

    return xs, ys


def get_galaxies(lines):
    galaxies = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                galaxies.append((x, y))

    return galaxies


def calc_distances(lines, expansion_factor):
    xs, ys = get_empties(lines)

    sums = 0
    galaxies = get_galaxies(lines)
    for i, (x1, y1) in enumerate(galaxies):
        for x2, y2 in galaxies[i:]:
            dist = abs(x1 - x2) + abs(y1 - y2)
            dist += len([x for x in xs if min(x1, x2) < x < max(x1, x2)]) * expansion_factor
            dist += len([y for y in ys if min(y1, y2) < y < max(y1, y2)]) * expansion_factor
            sums += dist

    return sums


def p1(lines):
    return calc_distances(lines, 1)


def p2(lines):
    return calc_distances(lines, 999_999)


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "11.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
