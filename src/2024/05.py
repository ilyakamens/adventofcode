#!/usr/bin/env python

"""https://adventofcode.com/2024/day/5."""

from collections import defaultdict
from functools import cmp_to_key

from main import main, runs


@runs(cases={'1'})
def p1(input: str) -> int:
    must_be_after = defaultdict(set)
    must_be_before = defaultdict(set)

    first, second = input.split('\n\n')
    for line in first.splitlines():
        before, after = line.split('|')
        must_be_after[before].add(after)
        must_be_before[after].add(before)

    middle_nums = []
    for line in second.splitlines():
        nums = line.split(',')
        for i, x in enumerate(nums):
            for j, y in enumerate(nums[i + 1 :]):
                if x in must_be_after[y] or y in must_be_before[x]:
                    break
            else:
                continue
            break
        else:
            middle_nums.append(nums[len(nums) // 2])

    return sum((int(x) for x in middle_nums))


@runs(cases={'1'})
def p2(input: str) -> int:
    must_be_after = defaultdict(set)
    must_be_before = defaultdict(set)

    first, second = input.split('\n\n')
    for line in first.splitlines():
        before, after = line.split('|')
        must_be_after[before].add(after)
        must_be_before[after].add(before)

    def sorter(a, b):
        if a in must_be_after[b]:
            return -1
        if b in must_be_before[a]:
            return 1
        return 0

    middle_nums = []
    for line in second.splitlines():
        nums = line.split(',')
        for i, x in enumerate(nums):
            for j, y in enumerate(nums[i + 1 :]):
                if x in must_be_after[y] or y in must_be_before[x]:
                    nums.sort(key=cmp_to_key(sorter))
                    middle_nums.append(nums[len(nums) // 2])
                    break
            else:
                continue
            break
        else:
            continue

    return sum((int(x) for x in middle_nums))


if __name__ == '__main__':
    main(p1, p2, [143], [123])
