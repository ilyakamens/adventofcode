#!/usr/bin/env python

"""https://adventofcode.com/2022/day/09."""

from collections import *
import copy
from os.path import abspath, dirname, join
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from utils import *


def iter_moves(moves):
    for move in moves:
        l, r = move.split(" ")
        if l == "U":
            dir = 1
            dist = int(r)
            sign = 1
        elif l == "R":
            dir = 0
            dist = int(r)
            sign = 1
        elif l == "D":
            dir = 1
            dist = int(r)
            sign = -1
        elif l == "L":
            dir = 0
            dist = int(r)
            sign = -1

        for _ in range(dist):
            yield dir, sign


def p1(moves):
    visited = {(0, 0)}

    h = [0, 0]
    t = [0, 0]
    for dir, sign in iter_moves(moves):
        h[dir] += sign
        if abs(h[0] - t[0]) + abs(h[1] - t[1]) > 2:
            x = h[0] - t[0]
            y = h[1] - t[1]
            t[0] += abs(x) // x
            t[1] += abs(y) // y
        elif abs(h[dir] - t[dir]) > 1:
            t[dir] += sign
        visited.add(tuple(t))

    return len(visited)


def p2(moves):
    visited = {(0, 0)}

    rope = [[0, 0] for _ in range(10)]

    for dir, sign in iter_moves(moves):
        rope[0][dir] += sign

        for i in range(1, 10):
            l, r = rope[i - 1], rope[i]
            x = l[0] - r[0]
            y = l[1] - r[1]
            if abs(x) + abs(y) > 2:
                r[0] += (abs(x) // x) if x != 0 else 0
                r[1] += (abs(y) // y) if y != 0 else 0
            elif abs(x) > 1:
                r[0] += abs(x) // x
            elif abs(y) > 1:
                r[1] += abs(y) // y

        visited.add(tuple(r))

    return len(visited)


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "09.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
