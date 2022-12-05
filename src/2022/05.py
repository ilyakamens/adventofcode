#!/usr/bin/env python

"""https://adventofcode.com/2022/day/05."""

from collections import *
from os.path import abspath, dirname, join
import re
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from utils import *


def intialize(starting_position):
    columns = [deque() for _ in starting_position.pop().split()]

    for row in starting_position:
        for i, column in enumerate(columns):
            try:
                crate = row[i + 1 + (i * 3)].strip()
            except IndexError:
                continue
            if crate:
                column.appendleft(crate)

    return columns


def move_crates(columns, moves, reverse=False):
    for move in moves:
        n, f, t = [int(n) for n in re.findall(r"\d+", move)]
        to_move = [columns[f - 1].pop() for _ in range(n)]
        columns[t - 1].extend(reversed(to_move) if reverse else to_move)

    return "".join([col[-1] for col in columns])


def p1(starting_position, moves):
    columns = intialize(starting_position)
    return move_crates(columns, moves)


def p2(starting_position, moves):
    columns = intialize(starting_position)
    return move_crates(columns, moves, reverse=True)


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "05.txt")) as f:
        start, moves = f.read().split("\n\n")

    for num, func in ((1, p1), (2, p2)):
        print(f"Part {num}: {func(start.splitlines(), moves.splitlines())}")
