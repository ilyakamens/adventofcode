#!/usr/bin/env python

"""https://adventofcode.com/2023/day/13."""

from os.path import abspath, dirname, join
import sys

sys.path.append(dirname(dirname(abspath(__file__))))


def vertical(pattern: list[list[str]]) -> int:
    verticles: list[int] = []

    prev: list[str] = []
    for x in range(len(pattern[0])):
        cur: list[str] = []
        for y in range(len(pattern)):
            cur.append(pattern[y][x])
        if prev == cur:
            verticles.append((x - 1, x))
        prev = cur

    def helper(l, r):
        while l >= 0 and r < len(pattern[0]):
            for y in range(len(pattern)):
                if pattern[y][l] != pattern[y][r]:
                    return False
            l -= 1
            r += 1

        return True

    for l, r in verticles:
        if helper(l, r):
            yield r


def horizontal(pattern: list[list[str]]) -> int:
    horizontals: list[int] = []

    prev: list[str] = []
    for y, cur in enumerate(pattern):
        if prev == cur:
            horizontals.append((y - 1, y))
        prev = cur

    for horizontal in horizontals:
        u, d = horizontal

        while u >= 0 and d < len(pattern):
            if pattern[u] != pattern[d]:
                break
            u -= 1
            d += 1
        else:
            yield horizontal[1]


def p1(patterns):
    sums = 0

    for pattern in patterns:
        sums += next(vertical(pattern), 0)
        sums += next(horizontal(pattern), 0) * 100

    return sums


def p2(patterns):
    sums = 0

    mapping = {".": "#", "#": "."}

    for pattern in patterns:
        for line in pattern:
            found = True
            for i, c in enumerate(line):
                v1 = set(vertical(pattern))
                h1 = set(horizontal(pattern))

                line[i] = mapping[c]

                v2 = set(vertical(pattern))
                if v2 and v1 != v2:
                    sums += ((v2 ^ v1) & v2).pop()
                    break

                h2 = set(horizontal(pattern))
                if h2 and h1 != h2:
                    sums += ((h2 ^ h1) & h2).pop() * 100
                    break

                line[i] = c
            else:
                found = False

            if found:
                break

    return sums


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "13.txt")) as f:
        groups = f.read().split("\n\n")

    patterns = [group.strip().split("\n") for group in groups]
    for i, pattern in enumerate(patterns):
        pattern = [list(line) for line in pattern]
        patterns[i] = pattern

    print(f"Part 1: {p1(patterns)}")
    print(f"Part 2: {p2(patterns)}")
