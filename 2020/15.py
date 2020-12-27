#!/usr/bin/env python

"""https://adventofcode.com/2020/day/15."""

import os


def get_last_spoken(nums, turn):
    num_map = {}
    for i, n in enumerate(nums, start=1):
        num_map[n] = (i, None)

    last = n
    for i in range(i + 1, turn + 1):
        last = 0 if num_map[last][1] is None else num_map[last][0] - num_map[last][1]
        num_map[last] = (i, num_map[last][0] if last in num_map else None)

    return last


if __name__ == "__main__":
    with open(os.path.join("input", "15.txt")) as f:
        nums = [int(n) for n in f.read().strip().split(",")]

    print(f"Part 1: {get_last_spoken(nums, 2020)}")

    print(f"Part 2: {get_last_spoken(nums, 30_000_000)}")
