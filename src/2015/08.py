#!/usr/bin/env python

"""https://adventofcode.com/2015/day/08."""

from os.path import getsize
import os

if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input", "08.txt")
    with open(filename) as f:
        lines = f.read().splitlines()
        raw = sum(len(l) for l in lines)

    with open(filename, encoding="unicode_escape") as f:
        mem = len(f.read()) - (len(lines) * 3)

    print(f"Part 1: {raw - mem}")

    raw_encoded = 0
    for line in lines:
        raw_encoded += len(line)
        raw_encoded += 2  # New quotes
        raw_encoded += line.count('"')  # Double quotes
        raw_encoded += line.count("\\")  # Backslashes

    print(f"Part 2: {raw_encoded - raw}")
