#!/usr/bin/env python

"""https://adventofcode.com/2021/day/01."""

import os

def part_1(lines):
    count = 0

    prev = lines[0]
    for curr in lines[1:]:
        count += 1 if curr > prev else 0
        prev = curr

    return count

def part_2(lines):
    depths = []

    for i, line in enumerate(lines[2:], start=2):
        depths.append(lines[i - 2] + lines[i - 1] + line)

    return part_1(depths)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "01.txt")) as f:
        lines = [int(line) for line in f.read().splitlines()]

    print(f"Part 1: {part_1(lines)}")

    print(f"Part 2: {part_2(lines)}")
