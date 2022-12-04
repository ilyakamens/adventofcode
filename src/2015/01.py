#!/usr/bin/env python

"""https://adventofcode.com/2015/day/01."""

import os

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "01.txt")) as f:
        parens = f.read().strip()

    print(f"Part 1: {parens.count('(') - parens.count(')')}")

    pos = None
    floor = 0
    for i, paren in enumerate(parens, start=1):
        floor += 1 if paren == "(" else -1
        if floor == -1:
            pos = i
            break

    print(f"Part 2: {pos}")
