#!/usr/bin/env python

"""https://adventofcode.com/2024/day/5."""

from functools import cmp_to_key
from typing import Callable

from main import main, runs
from utils import numbers, paras


def gen_key(input: str) -> tuple[set[tuple[str, str]], Callable[[str, str], int]]:
    rules = {tuple(line.split('|')) for line in input.splitlines()}

    @cmp_to_key
    def key(a, b):
        if (a, b) in rules:
            return -1
        if (b, a) in rules:
            return 1

        return 0

    return key


@runs(cases={'1'})
def p1(input: str) -> int:
    rules, updates = paras(input)
    key = gen_key(rules)

    middle_sum = 0
    for line in updates.splitlines():
        nums = numbers(line, cast=False)
        middle_sum += int(nums[len(nums) // 2]) if sorted(nums, key=key) == nums else 0

    return middle_sum


@runs(cases={'1'})
def p2(input: str) -> int:
    rules, updates = paras(input)
    key = gen_key(rules)

    middle_sum = 0
    for line in updates.splitlines():
        nums = numbers(line, cast=False)
        sorted_nums = sorted(nums, key=key)
        middle_sum += int(sorted_nums[len(nums) // 2]) if sorted_nums != nums else 0

    return middle_sum


if __name__ == '__main__':
    main(p1, p2, [143], [123])
