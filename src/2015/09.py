#!/usr/bin/env python

"""https://adventofcode.com/2015/day/09."""

from collections import defaultdict
from itertools import permutations
import os
import sys


def calc_distance(locs):
    return sum(dist[loc][locs[i + 1]] for i, loc in enumerate(locs[:-1]))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "09.txt")) as f:
        lines = f.read().splitlines()

    dist = defaultdict(dict)
    locs = set()
    for line in lines:
        a, _, b, _, distance = line.split(" ")
        dist[a][b] = int(distance)
        dist[b][a] = int(distance)
        locs.update([a, b])

    dists = [calc_distance(perm) for perm in permutations(locs)]
    print(f"Part 1: {min(dists)}")
    print(f"Part 2: {max(dists)}")
