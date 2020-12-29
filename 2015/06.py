#!/usr/bin/env python

"""https://adventofcode.com/2015/day/06."""

from collections import defaultdict
import os
import re


def iter_lights(start, stop):
    for x in range(start[0], stop[0] + 1):
        for y in range(start[1], stop[1] + 1):
            yield x, y


def change_lights_part_one(grid, start, stop, toggle):
    for x, y in iter_lights(start, stop):
        grid[f"{x},{y}"] = True if toggle else False if toggle is False else not grid[f"{x},{y}"]


def change_lights_part_two(grid, start, stop, inc):
    for x, y in iter_lights(start, stop):
        grid[f"{x},{y}"] += inc
        if grid[f"{x},{y}"] < 0:
            grid[f"{x},{y}"] = 0


def parse_lines(lines):
    parsed = []
    for l in lines:
        split = l.split(" ")
        start = [int(n) for n in split[-3].split(",")]
        stop = [int(n) for n in split[-1].split(",")]
        toggle, inc = (True, 1) if "on" in l else (False, -1) if "off" in l else (None, 2)
        parsed.append((start, stop, toggle, inc))

    return parsed


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "06.txt")) as f:
        lines = f.read().splitlines()

    grid = defaultdict(bool)
    for instruction in parse_lines(lines):
        start, stop, toggle, _ = instruction
        change_lights_part_one(grid, start, stop, toggle)

    print(f"Part 1: {len([v for v in grid.values() if v])}")

    grid = defaultdict(int)
    for instruction in parse_lines(lines):
        start, stop, _, inc = instruction
        change_lights_part_two(grid, start, stop, inc)

    print(f"Part 2: {sum(grid.values())}")
