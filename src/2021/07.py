#!/usr/bin/env python

"""https://adventofcode.com/2021/day/07."""

import os
import sys

def calc(nums, middle):
    sum_ = 0
    for num in nums:
        sum_ += abs(num - middle)
    return sum_

def p1(lines):
    nums = sorted([int(n) for n in lines[0].split(',')])
    middle_a = len(nums) // 2
    middle_b = middle_a - 1

    return min(calc(nums, nums[middle_a]), calc(nums, nums[middle_b]))

def calc2(nums, middle):
    sum_ = 0
    for num in nums:
        diff = abs(num - middle)
        sum_ += (diff * (diff + 1)) // 2
    return sum_

def p2(lines):
    nums = sorted([int(n) for n in lines[0].split(',')])

    best = sys.maxsize
    for i in range(nums[-1]):
        n = calc2(nums, i + 1)
        best = min(n, best)

    return best


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "07.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")

    print(f"Part 2: {p2(lines)}")
