#!/usr/bin/env python

"""https://adventofcode.com/2015/day/17."""

from collections import defaultdict
from itertools import combinations

from main import main, runs
from utils import numbers


def iter_combos(containers: list[int], liters: int):
    for i in range(len(containers)):
        for combo in combinations(containers, i):
            if sum(combo) == liters:
                yield combo


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    liters = {'1': 25, 'real': 150}[case]

    count = 0
    for _ in iter_combos(numbers(input), liters):
        count += 1

    return count


@runs(cases={'1'})
def p2(input: str, case: str) -> int:
    liters = {'1': 25, 'real': 150}[case]

    counts = defaultdict(int)
    for combo in iter_combos(numbers(input), liters):
        counts[len(combo)] += 1

    return counts[min(counts.keys())]


if __name__ == '__main__':
    main(p1, p2, [4], [3])
