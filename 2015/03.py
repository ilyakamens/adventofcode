#!/usr/bin/env python

"""https://adventofcode.com/2015/day/03."""

import os

mapping = {
    "^": (0, 1),
    ">": (1, 0),
    "v": (0, -1),
    "<": (-1, 0),
}


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input", "03.txt")) as f:
        directions = f.read().strip()

    houses = {(0, 0): True}
    pos = (0, 0)
    houses[pos] = True
    for d in directions:
        pos = tuple(sum(t) for t in zip(pos, mapping[d]))
        houses[pos] = True

    print(f"Part 1: {len(houses)}")

    houses = {(0, 0): True}
    santa_moves = [d for i, d in enumerate(directions) if i % 2 == 0]
    robot_moves = [d for i, d in enumerate(directions) if i % 2 != 0]
    for moves in (santa_moves, robot_moves):
        pos = (0, 0)
        for d in moves:
            pos = tuple(sum(t) for t in zip(pos, mapping[d]))
            houses[pos] = True

    print(f"Part 2: {len(houses)}")
