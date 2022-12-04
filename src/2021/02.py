#!/usr/bin/env python

"""https://adventofcode.com/2021/day/02."""

import os

def part_1(lines):
    h, d = 0, 0

    for l in lines:
        x, y = l.split()
        if x == 'forward':
            d += int(y)
        elif x == 'down':
            h += int(y)
        elif x == "up":
            h -= int(y)

    return h * d

def part_2(lines):
    h, d, aim = 0, 0, 0

    for l in lines:
        x, y = l.split()
        y = int(y)
        if x == 'forward':
            h += y
            d += aim * y
        elif x == 'down':
            aim += y
        elif x == "up":
            aim -= y

    return h * d


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "02.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {part_1(lines)}")

    print(f"Part 2: {part_2(lines)}")
