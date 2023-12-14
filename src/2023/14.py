#!/usr/bin/env python

"""https://adventofcode.com/2023/day/14."""

from os.path import abspath, dirname, join
import sys

sys.path.append(dirname(dirname(abspath(__file__))))


def rotateright(matrix):
    return [list(l) for l in list(zip(*matrix[::-1]))]


def rotateleft(matrix):
    return [list(l) for l in list(zip(*matrix))[::-1]]


def roll(m):
    for l in m:
        for i, c in enumerate(l[1:], start=1):
            if c != "O":
                continue
            while i > 0 and l[i - 1] == ".":
                l[i - 1], l[i] = l[i], l[i - 1]
                i -= 1


def p1(m):
    m = rotateleft(m)
    roll(m)

    return sum(l.count("O") * i for i, l in enumerate(rotateleft(m), start=1))


def p2(m):
    scores = []

    m = rotateleft(rotateleft(m))
    for j in range(1_000_000_000):
        if j >= 1_000 and j % 1_000 == 0:
            score = sum(l.count("O") * i for i, l in enumerate(m, start=1))
            if score not in scores:
                scores.append(score)
                # Only 21 scores are needed to find the pattern.
                print(score)
            else:
                break

        for _ in range(4):
            m = rotateright(m)
            roll(m)

    return scores[((1_000_000_000 % (len(scores) * 1_000)) - 1_000) // 1_000]


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "14.txt")) as f:
        lines = [list(l) for l in f.read().splitlines()]

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
