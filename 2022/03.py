#!/usr/bin/env python

"""https://adventofcode.com/2022/day/03."""

import os

ASCII_A = 97


def priority(s):
    return ord(s.lower()) - (ASCII_A - 1) + (26 if s.isupper() else 0)


def p1(lines):
    total_priority = 0

    for sack in lines:
        left, right = sack[: len(sack) // 2], sack[len(sack) // 2 :]
        dupe = (set(list(left)) & set(list(right))).pop()
        total_priority += priority(dupe)

    return total_priority


def chunks(list, size):
    for i in range(0, len(list), size):
        yield list[i : i + size]


def p2(lines):
    total_priority = 0

    for group in chunks(lines, 3):
        sets = [set(list(e)) for e in group]
        dupe = (sets[0] & sets[1] & sets[2]).pop()
        total_priority += priority(dupe)

    return total_priority


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "03.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
