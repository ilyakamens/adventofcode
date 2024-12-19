#!/usr/bin/env python

"""https://adventofcode.com/2024/day/19."""

from functools import cache

from main import main
from utils import paras


def parse(input: str) -> tuple[tuple[str], list[str]]:
    patterns, desireds = paras(input)
    patterns = tuple(patterns.split(', '))
    desireds = desireds.splitlines()

    return patterns, desireds


@cache
def match_count(patterns: list[str], desired: str) -> int:
    if not desired:
        return 1

    count = 0
    for p in patterns:
        if desired.startswith(p):
            count += match_count(patterns, desired[len(p) :])

    return count


def p1(input: str) -> int:
    patterns, desireds = parse(input)

    matches = 0
    for desired in desireds:
        if match_count(patterns, desired) > 0:
            matches += 1

    return matches


def p2(input: str) -> int:
    patterns, desireds = parse(input)

    matches = 0
    for desired in desireds:
        matches += match_count(patterns, desired)

    return matches


if __name__ == '__main__':
    main(p1, p2)
