#!/usr/bin/env python

"""https://adventofcode.com/2020/day/9."""

from collections import deque
import os


def find_first_not_sum(nums):
    prev_list = deque(nums[:25])
    prev_map = {prev: True for prev in prev_list}
    for num in nums[25:]:
        if not any([num - prev in prev_map or prev - num in prev_map for prev in prev_list]):
            return num
        del prev_map[prev_list.popleft()]
        prev_list.append(num)
        prev_map[num] = True


def find_summing_elements(needle, haystack):
    for n in range(2, len(haystack)):
        for i in range(0, len(haystack) - n):
            contig = haystack[i : i + n]
            if sum(contig) == needle:
                return contig


if __name__ == "__main__":
    with open(os.path.join("input", "09.txt")) as f:
        nums = [int(line) for line in f.read().splitlines()]

    first_not_sum = find_first_not_sum(nums)
    print(f"Part 1: {first_not_sum}")

    summing_elements = find_summing_elements(first_not_sum, nums)
    print(f"Part 2: {min(summing_elements) + max(summing_elements)}")
