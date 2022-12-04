#!/usr/bin/env python

"""https://adventofcode.com/2015/day/07."""

import os

ops = {
    "AND": "&",
    "OR": "|",
    "RSHIFT": ">>",
    "LSHIFT": "<<",
}

cache = {}


def signal(sigs, wire):
    if wire in cache:
        return cache[wire]
    if wire not in sigs:
        return int(wire)

    parts = sigs[wire].split(" ")

    if len(parts) == 1:
        cache[wire] = signal(sigs, parts[0])
    elif len(parts) == 2:
        cache[wire] = ~signal(sigs, parts[1])
    else:
        cache[wire] = eval(f"signal(sigs, parts[0]) {ops[parts[1]]} signal(sigs, parts[2])")

    return cache[wire]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "07.txt")) as f:
        lines = f.read().splitlines()

    sigs = {}
    for l in lines:
        left, right = l.split(" -> ")
        sigs[right] = left

    a = signal(sigs, "a")
    print(f"Part 1: {a}")

    cache = {}
    sigs["b"] = str(a)
    print(f"Part 2: {signal(sigs, 'a')}")
