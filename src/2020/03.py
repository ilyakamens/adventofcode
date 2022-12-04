#!/usr/bin/env python

"""https://adventofcode.com/2020/day/3."""

import os

from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])


def get_num_trees_for_slope(map_, slope):
    pos = Coordinate(0, 0)

    num_trees = 0
    while pos.y < len(map_):
        if pos.x >= len(map_[0]):
            pos = Coordinate(pos.x % len(map_[0]), pos.y)
        if map_[pos.y][pos.x] == "#":
            num_trees += 1
        pos = Coordinate(pos.x + slope.x, pos.y + slope.y)

    return num_trees


if __name__ == "__main__":
    with open(os.path.join("input", "03.txt")) as f:
        map_ = f.read().splitlines()

    # Part 1: Compute the number trees encountered given a map of trees and slope.
    num_trees = get_num_trees_for_slope(map_, Coordinate(3, 1))
    print(f"Number of trees encountered (part 1): {num_trees}")

    # Part 2: Compute the product of the number of trees encountered for each of the slopes.
    num_trees = 1
    for x, y in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        num_trees *= get_num_trees_for_slope(map_, Coordinate(x, y))

    print(f"Number of trees encountered (part 2): {num_trees}")
