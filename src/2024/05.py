#!/usr/bin/env python

"""https://adventofcode.com/2024/day/5."""

from collections import defaultdict
from functools import cmp_to_key
from itertools import combinations

from main import main, runs


def gen_rules(input: str) -> list[str]:
    must_be_after = defaultdict(set)
    must_be_before = defaultdict(set)

    for line in input.splitlines():
        before, after = line.split('|')
        must_be_after[before].add(after)
        must_be_before[after].add(before)

    return must_be_before, must_be_after


def is_valid(must_be_before, must_be_after, nums: list[str]) -> bool:
    for x, y in combinations(nums, 2):
        if x in must_be_after[y] or y in must_be_before[x]:
            return False

    return True


@runs(cases={'1'})
def p1(input: str) -> int:
    first, second = input.split('\n\n')
    must_be_before, must_be_after = gen_rules(first)

    middle_sum = 0
    for line in second.splitlines():
        nums = line.split(',')
        if is_valid(must_be_before, must_be_after, nums):
            middle_sum += int(nums[len(nums) // 2])

    return middle_sum


@runs(cases={'1'})
def p2(input: str) -> int:
    first, second = input.split('\n\n')
    must_be_before, must_be_after = gen_rules(first)

    def key(a, b):
        if a in must_be_after[b]:
            return -1
        if b in must_be_before[a]:
            return 1

        return 0

    middle_sum = 0
    for line in second.splitlines():
        nums = line.split(',')
        if not is_valid(must_be_before, must_be_after, nums):
            nums.sort(key=cmp_to_key(key))
            middle_sum += int(nums[len(nums) // 2])

    return middle_sum


if __name__ == '__main__':
    main(p1, p2, [143], [123])
