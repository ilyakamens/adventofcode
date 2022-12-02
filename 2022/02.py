#!/usr/bin/env python

"""https://adventofcode.com/2022/day/02."""

import os

CONVERT = {"X": "A", "Y": "B", "Z": "C"}
RANK = {"A": 1, "B": 2, "C": 3}


def evaluate(h1, h2):
    if h1 == h2:
        return 3

    return {"A": {"B": 6}, "B": {"C": 6}, "C": {"A": 6}}[h1].get(h2, 0)


def play(lines, p2=False):
    score = 0

    for round in lines:
        h1, h2 = round.split()
        h2 = DECRYPT[h2](h1) if p2 else CONVERT[h2]
        score += evaluate(h1, h2) + RANK[h2]

    return score


# Part 2
WIN = {"A": "B", "B": "C", "C": "A"}
LOSE = {v: k for k, v in WIN.items()}
DECRYPT = {
    "X": lambda h: LOSE[h],
    "Y": lambda h: h,
    "Z": lambda h: WIN[h],
}


def p1(lines):
    return play(lines)


def p2(lines):
    return play(lines, p2=True)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "02.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
