#!/usr/bin/env python

"""https://adventofcode.com/2022/day/01."""

import os

def parse(lines):
    return sorted([sum(int(c) for c in elf.split("\n") if c) for elf in lines], reverse=True)

def p1(lines):
    return parse(lines)[0]

def p2(lines):
    return sum(parse(lines)[:3])


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "01.txt")) as f:
        lines = f.read().split("\n\n")

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
