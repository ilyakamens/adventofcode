#!/usr/bin/env python

"""https://adventofcode.com/2023/day/08."""

import math
from os.path import abspath, dirname, join
import sys

sys.path.append(dirname(dirname(abspath(__file__))))


def parse(lines):
    pattern = lines[0].strip()

    mapping = {}
    for line in lines[2:]:
        k, r = line.split(" = ")
        l, r = r.split(", ")
        mapping[k] = dict(L=l[1:], R=r[:-1])

    return pattern, mapping


def p1(lines):
    pattern, mapping = parse(lines)

    i = 0
    cur = "AAA"
    while cur != "ZZZ":
        direction = pattern[i % len(pattern)]
        cur = mapping[cur][direction]
        i += 1

    return i


def p2(lines):
    pattern, mapping = parse(lines)

    nodes = []
    for k in mapping.keys():
        if k.endswith("A"):
            nodes.append(k)

    counts = [0] * len(nodes)

    i = 0
    while not all(n.endswith("Z") for n in nodes):
        direction = pattern[i % len(pattern)]
        for j, node in enumerate(nodes):
            if node.endswith("Z"):
                continue

            counts[j] += 1
            nodes[j] = mapping[node][direction]
        i += 1

    return math.lcm(*counts)


if __name__ == "__main__":
    with open(join(dirname(__file__), "input", "08.txt")) as f:
        lines = f.read().splitlines()

    print(f"Part 1: {p1(lines)}")
    print(f"Part 2: {p2(lines)}")
