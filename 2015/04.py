#!/usr/bin/env python

"""https://adventofcode.com/2015/day/04."""

from hashlib import md5
import os


def find_starts_with(secret, string):
    n = 1
    while not md5(f"{secret}{n}".encode("utf-8")).hexdigest().startswith(string):
        n += 1

    return n


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "04.txt")) as f:
        secret = f.read().strip()

    print(f"Part 1: {find_starts_with(secret, '0' * 5)}")

    print(f"Part 2: {find_starts_with(secret, '0' * 6)}")
