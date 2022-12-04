#!/usr/bin/env python

"""https://adventofcode.com/2020/day/25."""

import os


def crack(num_loops=None, key=None, subject=7):
    value = 1
    loop_size = 0
    while (key is not None and value != key) or (num_loops is not None and num_loops != loop_size):
        value *= subject
        value %= 20201227
        loop_size += 1

    return value if num_loops is not None else loop_size


if __name__ == "__main__":
    with open(os.path.join("input", "25.txt")) as f:
        pub_keys = [int(k) for k in f.read().splitlines()]

    loop_size = crack(key=pub_keys[0])
    key = crack(num_loops=loop_size, subject=pub_keys[1])
    print(f"Day 25: {key}")
