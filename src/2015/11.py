#!/usr/bin/env python

"""https://adventofcode.com/2015/day/11."""

import copy
from itertools import groupby
import os


def consec(chunk):
    return ord(chunk[0]) + 1 == ord(chunk[1]) == ord(chunk[2]) - 1


def valid(password):
    if any(char in password for char in ("i", "o", "l")):
        return False

    if not any(consec(password[i : i + 3]) for i in range(len(password) - 2)):
        return False

    return len([_ for _, grouper in groupby(password) if len(list(grouper)) > 1]) > 1


def inc(password):
    new = copy.copy(password)
    while not valid(new) or new == password:
        i = -1
        val = ord(new[i]) + 1
        while val > ord("z"):
            new[i] = "a"
            i -= 1
            val = ord(new[i]) + 1
        new[i] = chr(val)

    return "".join(new)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "11.txt")) as f:
        password = list(f.read().strip())

    print(f"Part 1: {inc(password)}")
    print(f"Part 2: {inc(list(inc(password)))}")
