#!/usr/bin/env python

"""https://adventofcode.com/2021/day/06."""

from collections import defaultdict
import os

def p1(lines):
    fishes = [int(f) for f in lines[0].split(",")]
    for _ in range(80):
        for i, fish in enumerate(fishes):
            if fish == 0:
                fishes[i] = 6
                fishes.append(9)
                continue
            fishes[i] = fish - 1

    return len(fishes)

def p2(lines):
    split = [int(f) for f in lines[0].split(",")]
    fishes = [0 for _ in range(9)]
    for n in split:
        fishes[n] += 1
    for _ in range(256):
        add_count = 0
        for i, c in enumerate(fishes):
            if i == 0:
                add_count = c
                fishes[0] = 0
                continue
            fishes[i - 1] += c
            fishes[i] = 0
        fishes[8] += add_count
        fishes[6] += add_count

    return sum(fishes)

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "06.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
