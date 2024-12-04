#!/usr/bin/env python

"""https://adventofcode.com/2024/day/4."""

from collections import defaultdict
from typing import Annotated

from main import main

run_type = Annotated[str, '1, 2, 3, etc., or real']


def check_square(m, i, j):
    count = 0
    if m[i][j] + m[i + 1][j] + m[i + 2][j] + m[i + 3][j] == 'XMAS':
        count += 1
    if m[i][j] + m[i - 1][j] + m[i - 2][j] + m[i - 3][j] == 'XMAS':
        count += 1
    if m[i][j] + m[i][j + 1] + m[i][j + 2] + m[i][j + 3] == 'XMAS':
        count += 1
    if m[i][j] + m[i][j - 1] + m[i][j - 2] + m[i][j - 3] == 'XMAS':
        count += 1
    if m[i][j] + m[i + 1][j + 1] + m[i + 2][j + 2] + m[i + 3][j + 3] == 'XMAS':
        count += 1
    if m[i][j] + m[i + 1][j - 1] + m[i + 2][j - 2] + m[i + 3][j - 3] == 'XMAS':
        count += 1
    if m[i][j] + m[i - 1][j - 1] + m[i - 2][j - 2] + m[i - 3][j - 3] == 'XMAS':
        count += 1
    if m[i][j] + m[i - 1][j + 1] + m[i - 2][j + 2] + m[i - 3][j + 3] == 'XMAS':
        count += 1

    return count


def p1(run: run_type, input: str) -> int:
    m = defaultdict(lambda: defaultdict(str))
    for i, line in enumerate(input.splitlines()):
        for j, c in enumerate(line):
            m[i][j] = c

    count = 0
    for i in range(len(m) + 1):
        for j in range(len(m[i]) + 1):
            count += check_square(m, i, j)

    return count


def p2(run: run_type, input: str) -> int:
    m = defaultdict(lambda: defaultdict(str))
    for i, line in enumerate(input.splitlines()):
        for j, c in enumerate(line):
            m[i][j] = c

    count = 0
    for i in range(len(m)):
        for j in range(len(m[i])):
            count += check2(m, i, j)

    return count


def check2(m, i, j):
    if m[i][j] != 'A':
        return 0
    if (
        m[i + 1][j + 1] == 'M'
        and m[i + 1][j - 1] == 'M'
        and m[i - 1][j - 1] == 'S'
        and m[i - 1][j + 1] == 'S'
    ):
        return 1
    if (
        m[i + 1][j - 1] == 'M'
        and m[i - 1][j - 1] == 'M'
        and m[i - 1][j + 1] == 'S'
        and m[i + 1][j + 1] == 'S'
    ):
        return 1
    if (
        m[i - 1][j - 1] == 'M'
        and m[i - 1][j + 1] == 'M'
        and m[i + 1][j + 1] == 'S'
        and m[i + 1][j - 1] == 'S'
    ):
        return 1
    if (
        m[i - 1][j + 1] == 'M'
        and m[i + 1][j + 1] == 'M'
        and m[i + 1][j - 1] == 'S'
        and m[i - 1][j - 1] == 'S'
    ):
        return 1

    return 0


if __name__ == '__main__':
    main(p1, p2, [18], [9])
