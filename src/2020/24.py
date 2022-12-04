#!/usr/bin/env python

"""https://adventofcode.com/2020/day/24."""

from collections import defaultdict
import itertools
import os
import re

STEPS = {
    "ne": (0.5, 1),
    "e": (1, 0),
    "se": (0.5, -1),
    "sw": (-0.5, -1),
    "w": (-1, 0),
    "nw": (-0.5, 1),
}


def iter_neighbors(tile):
    for x, y in STEPS.values():
        yield (tile[0] + x, tile[1] + y)


def should_flip(tile_map, tile):
    black_count = 0
    for neighbor in iter_neighbors(tile):
        black_count += 1 if tile_map.get(neighbor) else 0

    return black_count == 2 if not tile_map.get(tile) else black_count == 0 or black_count > 2


def apply_flips(tile_map):
    to_flip = {}
    visited = set()
    for tile, color in tile_map.items():
        for t in itertools.chain(iter_neighbors(tile), [tile]):
            if t not in visited and should_flip(tile_map, t):
                to_flip[t] = True
            visited.add(t)

    for tile in to_flip.keys():
        tile_map[tile] = not tile_map[tile]


def construct_map(tiles):
    tile_map = defaultdict(bool)
    for tile in tiles:
        dest = (0, 0)
        for step, mapping in STEPS.items():
            r = f"(?<![ns]){step}"
            count = len(re.findall(r, tile)) if step in {"e", "w"} else tile.count(step)
            dest = (dest[0] + mapping[0] * count, dest[1] + mapping[1] * count)
        tile_map[dest] = not tile_map[dest]

    return tile_map


if __name__ == "__main__":
    with open(os.path.join("input", "24.txt")) as f:
        tiles = f.read().splitlines()

    tile_map = construct_map(tiles)
    print(f"Part 1: {len([v for v in tile_map.values() if v])}")

    for i in range(100):
        apply_flips(tile_map)

    print(f"Part 2: {len([v for v in tile_map.values() if v])}")
