#!/usr/bin/env python

"""https://adventofcode.com/2024/day/7."""

from itertools import product
from typing import Callable, Generator

from main import main, runs
from utils import numbers


def add(l, r):
    return l + r


def mult(l, r):
    return l * r


def concat(l, r):
    return int(str(l) + str(r))


def iter_equations(
    input: str, ops: list[Callable]
) -> Generator[int, list[int], list[list[Callable]]]:
    for line in input.splitlines():
        test_val, *nums = numbers(line)
        yield test_val, nums, product(ops, repeat=len(nums) - 1)


def has_match(test_val: int, nums: list[int], opss: list[Callable]) -> bool:
    for ops in opss:
        total = nums[0]
        for num, op in zip(nums[1:], ops):
            total = op(total, num)
            if total > test_val:
                break
        if total == test_val:
            return True

    return False


@runs(cases={'1'})
def p1(input: str, case: str) -> int:
    total = 0
    for test_val, nums, opss in iter_equations(input, ops=[add, mult]):
        if has_match(test_val, nums, opss):
            total += test_val

    return total


@runs(cases={'1'})
def p2(input: str, case: str) -> int:
    total = 0
    for test_val, nums, opss in iter_equations(input, ops=[add, mult, concat]):
        if has_match(test_val, nums, opss):
            total += test_val

    return total


if __name__ == '__main__':
    main(p1, p2, [3749], [11387])
